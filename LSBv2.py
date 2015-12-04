#%matplotlib inline
import io
import os
from PIL import Image
import binascii
import os
import numpy
import matplotlib.pyplot as plt
import scipy
from scipy import fftpack
import urllib2
import struct

current_file_size_bytes = 0
image_theoretical_max_size = 0
Red = None
Green = None
Blue = None

#Metadata specifications
FILE_SIZE_HEADER_BITS = 32
FILE_NAME_SIZE_HEADER_BITS = 16
LSB_SIZE_BITS = 8
METADATA_LSB = 2

#Convert a decimal number to binary
def convert_decimal_binary(value):
    if value == 0: return "0"
    s = ''
    while value:
        if value & 1 == 1:
            s = "1" + s
        else:
            s = "0" + s
        value /= 2
    return s



def open_image(file_name, lsbs):
    """open an image for inserting data or extracting data"""
    global Red
    global Green
    global Blue
    global image_theoretical_max_size
    image = Image.open(file_name).convert('RGB')
    r, g, b = image.split()

    Red = numpy.array(r, dtype=numpy.float)
    Green = numpy.array(g, dtype=numpy.float)
    Blue = numpy.array(b, dtype=numpy.float)

    #Conversao dos DCT
    #Red = get_2D_dct(imgR)
    #Green = get_2D_dct(imgG)
    #Blue = get_2D_dct(imgB)

    image_theoretical_max_size = get_image_theoretical_max_available_size(lsbs)

    print "image theoretical max available size = " + str(image_theoretical_max_size/8) + " KBytes"
    #return image


    #out = Image.merge("RGB", (r, g, b))
    #out.save("merged.png")
    #print numpy.array(r, dtype=numpy.float)
    #img_color = image.resize(size, 1)

def get_image_theoretical_max_available_size(LSB_size):
    global Red
    global Green
    global Blue
    return ((Red.shape[0] * Red.shape[1] * LSB_size)/8) + ((Green.shape[0] * Green.shape[1] * LSB_size)/8) \
           + ((Blue.shape[0] * Blue.shape[1] * LSB_size)/8)

def open_file(filename):
    """Opens a file to be hidden in the current selected image"""
    global current_file_size_bytes
    with open(filename, 'rb') as f:
        content = f.read()
    st = os.stat(filename)
    current_file_size_bytes = st.st_size
    print "Selected file has: " +str(current_file_size_bytes/1024.0)+" KBytes"
    return binascii.hexlify(content)


def utf8_to_bin(text):
    return '{:b}'.format(int(text.encode('utf-8').encode('hex'), 16))


def bin_to_utf8(bits):
    return ('%x' % int(bits, 2)).decode('hex').decode('utf-8')

def byte_to_binary(n):
    return ''.join(str((n & (1 << i)) and 1) for i in reversed(range(8)))

def hex_to_binary(h):
    return ''.join(byte_to_binary(ord(b)) for b in binascii.unhexlify(h))


def get_reconstructed_image(raw):
    """Converts a numpy.ndarray image type to PIL"""
    img = raw.clip(0, 255)
    img = img.astype('uint8')
    img = Image.fromarray(img)
    return img

def replace_last_bit(binary_coef_number, binary_number):
    return binary_coef_number[:-1] + binary_number


#converte o float64 num inteiro 
def convert_float64_int(dct):
   return dct.astype(numpy.int64)

#converte o inteiro num float64
def convert_int_float64(inteiro):
    return inteiro.astype(numpy.float64)

def float_to_bin(f):
    """ convert float to binary string """
    ba = struct.pack('>d', f)
    s = ''.join('{:08b}'.format(ord(b)) for b in ba)
    # strip off leading zeros
    for i in range(len(s)):
        if s[i] != '0':
            break
    else:  # all zeros
        s = '0'
        i = 0
    return s[i:]

def int_to_bytes(n, minlen=0):  # helper function
    """ int/long to byte string """
    nbits = n.bit_length() + (1 if n < 0 else 0)  # plus one for any sign bit
    nbytes = (nbits+7)/8  # number of whole bytes
    bytes = []
    for i in range(nbytes):
        bytes.append(chr(n & 0xff))
        n >>= 8
    # zero pad if needed
    if minlen > 0 and len(bytes) < minlen:
        bytes.extend((minlen-len(bytes)) * '0')
    bytes.reverse()  # put high bytes at beginning
    return ''.join(bytes)

def bin_to_float(b):
    """ convert binary string to float """
    bf = int_to_bytes(int(b, 2), 8)  # 8 bytes needed for IEEE 754 binary64
    return struct.unpack('>d', bf)[0]

def add_padding(message_size_bin, padd_size):
    while len(message_size_bin) < padd_size:
        message_size_bin = "0" + message_size_bin
    return message_size_bin

def write_bits(bits_list, lsb, i, j):
    """Writes a bit list in the current selected image starting from pixel(i,j) using
    the lsb (least significant bits) parameter to specify the number of bits to be overwritten
     for each pixel"""
    line_size = Red.shape[0] - 1
    column_size = Red.shape[1] - 1
    last = False
    total_bits = len(bits_list)
    count = 0
    while i < line_size:
        while j < column_size:
            if count < total_bits:

                binImgR = convert_decimal_binary(int(Red[i][j]))
                binImgG = convert_decimal_binary(int(Green[i][j]))
                binImgB = convert_decimal_binary(int(Blue[i][j]))
                #print "Antes: "+ binImgR + " - " +str(int(Red[i][j]))
                Red[i][j] = int(""+binImgR[:-lsb] + ''.join(bits_list[count:count+lsb]), 2)
                #print "Depoi: " +binImgR[:-lsb] + ''.join(bits_list[count:count+lsb])
                count += lsb
                if count == total_bits:
                    last = True
                    break

                #print "Antes: "+ binImgG + " - " +str(int(Green[i][j]))
                Green[i][j] = int(""+binImgG[:-lsb] + ''.join(bits_list[count:count+lsb]), 2)
                #print "Depoi: " +binImgG[:-lsb] + ''.join(bits_list[count:count+lsb])
                count += lsb
                if count == total_bits:
                    last = True
                    break

                #print "Antes: "+ binImgB + " - " + str(int(Blue[i][j]))
                Blue[i][j] = int(""+binImgB[:-lsb] + ''.join(bits_list[count:count+lsb]), 2)
                #print "Depoi: " +binImgB[:-lsb] + ''.join(bits_list[count:count+lsb])
                count += lsb
                if count == total_bits:
                    last = True
                    break
                j+=1
            else:
                last = True
                break
        if last == True:
            break
        i+=1
        j=0
    return i, j

def check_bound(i, j):
    """For the case were the writing process stops at the edge of the image"""

    column_size = Red.shape[1] - 1
    if(j == column_size):
        i+=1
        j=0
    else:
        j+=1
    return i, j

def hide_metadata(file_size, file_name_size, lsb):
    """Here e write in te first pixels of the image the metadata referring to the file to be hidden
    """
    global FILE_SIZE_HEADER_BITS
    global METADATA_LSB
    global FILE_NAME_SIZE_HEADER_BITS
    global LSB_SIZE_BITS
    i = 0
    j = 0

    print "Data size = " + str(file_size)
    message_size_bin = convert_decimal_binary(file_size)
    message_size_bin_padd = add_padding(message_size_bin, FILE_SIZE_HEADER_BITS)
    #print "Data size bin = " + str(message_size_bin_padd)

    print "file_name_size = " + str(file_name_size)
    file_name_size_bin = convert_decimal_binary(file_name_size)
    file_name_size_bin_padd = add_padding(file_name_size_bin, FILE_NAME_SIZE_HEADER_BITS)
    #print "file_name_size_bin = " + str(file_name_size_bin_padd)

    print "LSB_size = " + str(lsb)
    LSB_size_bin = convert_decimal_binary(lsb)
    LSB_size_bin_padd = add_padding(LSB_size_bin, LSB_SIZE_BITS)
    #print "LSB_size_bin_padd = " + str(LSB_size_bin_padd)

    message_size_bin_padd_list = list(message_size_bin_padd)
    file_name_size_bin_padd_list = list(file_name_size_bin_padd)
    LSB_size_bin_padd_list = list(LSB_size_bin_padd)


    i, j = write_bits(message_size_bin_padd_list, METADATA_LSB, i, j)
    i, j = check_bound(i, j)
    i, j = write_bits(file_name_size_bin_padd_list, METADATA_LSB, i, j)
    i, j = check_bound(i, j)
    i, j = write_bits(LSB_size_bin_padd_list, METADATA_LSB, i, j)
    i, j = check_bound(i, j)

    return i, j

def hide_file(file_name, lsb):

    """Process of hiding:
        -metadata
        -filename
        -file binary
    """
    global Red
    global Green
    global Blue
    file_hex = open_file(file_name)

    global image_theoretical_max_size
    image_theoretical_max_size = get_image_theoretical_max_available_size(lsb)
    #print current_file_size_bytes + ((FILE_SIZE_HEADER_BITS + FILE_NAME_SIZE_HEADER_BITS + LSB_SIZE_BITS)/8)
    if image_theoretical_max_size < (current_file_size_bytes + ((FILE_SIZE_HEADER_BITS + FILE_NAME_SIZE_HEADER_BITS + LSB_SIZE_BITS)/8)):
        print "Image to small for current selected file, try to change LSB value."
        raise ValueError('Image to small for current selected file, try to change LSB value')

    binary = hex_to_binary(file_hex)
    binary_list = list(binary)

    bin_file_name = utf8_to_bin(file_name)
    while len(bin_file_name)%lsb != 0:
        bin_file_name =  "0"+bin_file_name

    print "File has "+str(len(binary)/8)+" Bytes"
    i, j = hide_metadata(len(binary), len(bin_file_name), lsb)
    i, j = write_bits(list(bin_file_name), lsb, i, j)
    i, j = check_bound(i, j)
    i, j = write_bits(binary_list, lsb, i, j)
    i, j = check_bound(i, j)

    a=get_reconstructed_image(Red)
    b=get_reconstructed_image(Green)
    c=get_reconstructed_image(Blue)
    return Image.merge("RGB", (a, b, c))

def read_bits(i, j, lsb, bits_size):
    """Reads bits starting in pixel(i,j) up to bits_size"""
    result = list()
    line_size = Red.shape[0] - 1
    column_size = Red.shape[1] - 1
    last = False
    while i < line_size:
        while j < column_size:
            a = len(result)*lsb
            binImgR = convert_decimal_binary(int(Red[i][j]))
            binImgR = add_padding(binImgR, 8)
            binImgG = convert_decimal_binary(int(Green[i][j]))
            binImgG = add_padding(binImgG, 8)
            binImgB = convert_decimal_binary(int(Blue[i][j]))
            binImgB = add_padding(binImgB, 8)
            result.append(binImgR[-lsb:])
            if len(result)*lsb == bits_size:
                last = True
                break

            result.append(binImgG[-lsb:])
            if len(result)*lsb == bits_size:
                last = True
                break

            result.append(binImgB[-lsb:])
            if len(result)*lsb == bits_size:
                last = True
                break
            j+=1

        if last == True:
            break
        i+=1
        j=0
    return result, i, j

def extract_metadata():
    """Process responsible for reading metadata from an image"""
    file_size_bin, i, j = read_bits(0, 0, METADATA_LSB, FILE_SIZE_HEADER_BITS)
    i, j = check_bound(i, j)
    file_name_size_bin, i, j = read_bits(i, j, METADATA_LSB, FILE_NAME_SIZE_HEADER_BITS)
    i, j = check_bound(i, j)
    lsb_bin, i, j = read_bits(i, j, METADATA_LSB, LSB_SIZE_BITS)
    i, j = check_bound(i, j)

    bin_size = ''.join(file_size_bin)
    file_name_size = ''.join(file_name_size_bin)
    lsb = ''.join(lsb_bin)

    return i, j, int(bin_size, 2), int(file_name_size, 2), int(lsb, 2)

def convert_bits_text(bits, encoding='utf-8', errors='surrogatepass'):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def save_file(filename, fileContent):
    file = open(filename, "wb")
    file.write(fileContent)
    file.close()

def extract(file_name):
    """Process responsible for reading:
        -Metadata
        -Filename
        -FileBinary
    """
    global Red
    global Green
    global Blue
    open_image(file_name, 0)
    i, j, bin_size, file_name_size, lsb = extract_metadata()
    file_name_bin, i, j = read_bits(i, j, lsb, file_name_size)
    file_namef =  bin_to_utf8(''.join(file_name_bin))
    i, j = check_bound(i, j)
    file_bin, i, j = read_bits(i, j, lsb, bin_size)
    newfile = convert_bits_text(''.join(file_bin))
    #save_file("a"+file_namef, newfile)
    return newfile, file_namef

# lsbs = 1
# open_image("Lenna.jpg", lsbs)
# print "------------------"
# out = hide_file("LennaS.jpg", lsbs)
# out.save("final.png", "PNG")
# print "=============="
# newFile, file_name = extract("final.png")
# save_file("a"+file_name, newFile)