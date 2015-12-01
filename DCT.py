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
dctRed = None
dctGreen = None
dctBlue = None

#Metadata specifications
FILE_SIZE_HEADER_BITS = 32
FILE_NAME_SIZE_HEADER_BITS = 16
LSB_SIZE_BITS = 8
METADATA_LSB = 4

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
    global dctRed
    global dctGreen
    global dctBlue
    global image_theoretical_max_size
    image = Image.open(file_name).convert('RGB')
    r, g, b = image.split()

    imgR = numpy.array(r, dtype=numpy.float)
    imgG = numpy.array(g, dtype=numpy.float)
    imgB = numpy.array(b, dtype=numpy.float)

    #Conversao dos DCT
    dctRed = get_2D_dct(imgR)
    dctGreen = get_2D_dct(imgG)
    dctBlue = get_2D_dct(imgB)

    image_theoretical_max_size = get_image_theoretical_max_size(dctRed, dctGreen, dctBlue, lsbs)

    print "image_theoretical_max_size = " + str(image_theoretical_max_size) + " Bytes"
    return image


    #out = Image.merge("RGB", (r, g, b))
    #out.save("merged.png")
    #print numpy.array(r, dtype=numpy.float)
    #img_color = image.resize(size, 1)

def get_image_theoretical_max_size(dctR, dctG, dctB, LSB_size):
    size_matrixR = dctR.shape[0]
    size_matrixG = dctG.shape[0]
    size_matrixB = dctB.shape[0]
    return ((size_matrixR * size_matrixR * LSB_size)/8) + ((size_matrixG * size_matrixG * LSB_size)/8) + \
           ((size_matrixB * size_matrixB * LSB_size)/8)

 

def get_2D_dct(img):
    """ Get 2D Cosine Transform of Image
    """
    return fftpack.dct(fftpack.dct(img.T, norm='ortho').T, norm='ortho')

def get_2d_idct(coefficients):
    """ Get 2D Inverse Cosine Transform of Image
    """
    return fftpack.idct(fftpack.idct(coefficients.T, norm='ortho').T, norm='ortho')

def open_file(filename):
    global current_file_size_bytes
    with open(filename, 'rb') as f:
        content = f.read()
    st = os.stat(filename)
    current_file_size_bytes = st.st_size
    return binascii.hexlify(content)


def utf8_to_bin(text):
    return '{:b}'.format(int(text.encode('utf-8').encode('hex'), 16))


def bin_to_utf8(bits):
    ('%x' % int(bits, 2)).decode('hex').decode('utf-8')

def byte_to_binary(n):
    return ''.join(str((n & (1 << i)) and 1) for i in reversed(range(8)))

def hex_to_binary(h):
    return ''.join(byte_to_binary(ord(b)) for b in binascii.unhexlify(h))


def get_reconstructed_image(raw):
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

# Convert message  into bits
def convert_message_to_binary(message):
    result = ''
    for c in message:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result = result + bits
    return result

def message_sliced(data_bin_list, lsb):
    data_aux = data_bin_list[0:lsb]
    print data_bin_list
    del data_bin_list[0:lsb]
    print data_bin_list
    print "data_aux" + ''.join(data_aux)
    if len(data_aux) != lsb:
        raise ValueError('Bits are over')
    return ''.join(data_aux)

def write_bits(bits_list, lsb, i, j):
    size = dctRed.shape[0]
    line_size = size - 1
    column_size = size - 1
    last = False
    while i < line_size:
        while j < column_size:
            if len(bits_list) > 0:
                binImgR = float_to_bin(dctRed[i][j])
                binImgG = float_to_bin(dctGreen[i][j])
                binImgB = float_to_bin(dctBlue[i][j])
                try:
                    print "Antes - "+str(float_to_bin(dctRed[i][j]))
                    dctRed[i][j] = bin_to_float(binImgR[:-lsb] + message_sliced(bits_list, lsb))
                    print "Depoi - "+str(float_to_bin(dctRed[i][j]))
                except:
                    pass
                try:
                    dctGreen[i][j] = bin_to_float(binImgG[:-lsb] + message_sliced(bits_list, lsb))
                except:
                    pass
                try:
                    dctBlue[i][j] = bin_to_float(binImgB[:-lsb] + message_sliced(bits_list, lsb))
                except:
                    pass
                j+=1
            else:
                last = True
                break
        if last == True:
            break
        i+=1
        j=0
    return i, j


def hide_metadata(size, file_name):
    global FILE_SIZE_HEADER_BITS
    global METADATA_LSB
    global FILE_NAME_SIZE_HEADER_BITS
    global LSB_SIZE_BITS
    i = 0
    j = 0

    print "size = " + str(size)
    message_size_bin = convert_decimal_binary(size)
    message_size_bin_padd = add_padding(message_size_bin, FILE_SIZE_HEADER_BITS)
    print "size2 = " + str(message_size_bin_padd)

    file_name_size_bin = convert_decimal_binary(len(utf8_to_bin(file_name)))
    file_name_size_bin_padd = add_padding(file_name_size_bin, FILE_NAME_SIZE_HEADER_BITS)

    LSB_size_bin = convert_decimal_binary(METADATA_LSB)
    LSB_size_bin_padd = add_padding(LSB_size_bin, LSB_SIZE_BITS)

    message_size_bin_padd_list = list(message_size_bin_padd)
    file_name_size_bin_padd_list = list(file_name_size_bin_padd)
    LSB_size_bin_padd_list = list(LSB_size_bin_padd)


    i, j = write_bits(message_size_bin_padd_list, METADATA_LSB, i, j)
    i, j = write_bits(file_name_size_bin_padd_list, METADATA_LSB, i, j)
    i, j = write_bits(LSB_size_bin_padd_list, METADATA_LSB, i, j)

    return i, j

def hide_file(file_name, lsb):
    file_hex = open_file(file_name)
    print image_theoretical_max_size
    print current_file_size_bytes + ((FILE_SIZE_HEADER_BITS + FILE_NAME_SIZE_HEADER_BITS + LSB_SIZE_BITS)/8)
    if image_theoretical_max_size < (current_file_size_bytes + ((FILE_SIZE_HEADER_BITS + FILE_NAME_SIZE_HEADER_BITS + LSB_SIZE_BITS)/8)):
        print "Image to small for current selected file, try to change LSB value."
        raise ValueError('Image to small for current selected file, try to change LSB value')

    binary = hex_to_binary(file_hex)
    binary_list = list(binary)

    bin_file_name = utf8_to_bin(file_name)

    global dctRed
    global dctGreen
    global dctBlue

    # print dctRed
    # print "===="
    # print dctGreen
    # print "===="
    # print dctBlue

    print "File has "+str(len(binary)/8)+" Bytes"
    i, j = hide_metadata(len(binary), file_name)

    i, j = write_bits(list(bin_file_name), lsb, i, j)
    i, j = write_bits(binary_list, lsb, i, j)



    # print i
    # print j
    # print dctRed
    # print "===="
    # print dctGreen
    # print "===="
    # print dctBlue
    #print '{0:.64f}'.format(dctBlue[5][8])
    a=get_reconstructed_image(get_2d_idct(dctRed))
    b=get_reconstructed_image(get_2d_idct(dctGreen))
    c=get_reconstructed_image(get_2d_idct(dctBlue))
    return Image.merge("RGB", (a, b, c))

def extract_metadata():
    file_size_bin = list()
    file_name_size_bin = list()
    lsb_bin = list()

    i = 0
    j = 0
    size = dctRed.shape[0]
    line_size = size - 1
    column_size = size - 1
    last = False
    while i < line_size:
        while j < column_size:

            binImgR = float_to_bin(dctRed[i][j])
            binImgG = float_to_bin(dctGreen[i][j])
            binImgB = float_to_bin(dctBlue[i][j])

            file_size_bin.append(binImgR[-METADATA_LSB:])
            if len(file_size_bin)*METADATA_LSB == FILE_SIZE_HEADER_BITS:
                last = True
                break

            file_size_bin.append(binImgG[-METADATA_LSB:])
            if len(file_size_bin)*METADATA_LSB == FILE_SIZE_HEADER_BITS:
                last = True
                break

            file_size_bin.append(binImgB[-METADATA_LSB:])
            if len(file_size_bin)*METADATA_LSB == FILE_SIZE_HEADER_BITS:
                last = True
                break
            j+=1

        if last == True:
            break
        i+=1
        j=0
    print file_size_bin
    bin_size = ''.join(file_size_bin)
    print bin_size
    print int(bin_size, 2)/8

def extract_message(file_name):
    global dctRed
    global dctGreen
    global dctBlue
    print float_to_bin(dctBlue[0][1])
    open_image(file_name, 0)
    extract_metadata()

  #extrai os dcts
    #extrair a metadata
    #extrair os bits menos significativos de cada dct 
    #assemblar todos 
    #imprimir a mensagem





lsbs = 55
open_image("Lenna.jpg", lsbs)
print float_to_bin(dctBlue[0][1])
out = hide_file("LennaS.jpg", lsbs)
print float_to_bin(dctBlue[0][1])
out.save("final.png")
print "=============="
extract_message("final.png")




#converte para binario (mas apenas mostra 32bits, e o tipo supostamente e  'numpy.float64')
#print ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', dct[0][0]))
#for i in range (0, dct_size):
    #dct[i][i] = 0

#print dct_size
# Reconstructed image
#idct = get_2d_idct(dct)
#reconstructed_image = get_reconstructed_image(idct)
#reconstructed_image.save("img.png")

#print numpy.array(reconstructed_image, dtype=numpy.float)
