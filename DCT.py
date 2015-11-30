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
FILE_NAME_SIZE_HEADER_BITS = 9
LSB_SIZE_BITS = 4

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


def open_image(file_name):
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

    image_theoretical_max_size = float(get_image_theoretical_max_size(dctRed, dctGreen, dctBlue, 4))/1024

    print "image_theoretical_max_size = " + str(image_theoretical_max_size) + " KBytes"
    return image


   # out = Image.merge("RGB", (r, g, b))
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

def add_padding(message_size_bin):

    while len(message_size_bin) < 32:
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


def message_size_bin_padd_sliced(message_size_bin_padd_list):
    message_aux = message_size_bin_padd_list[0:4]
    del message_size_bin_padd_list[0:4]
    if len(message_aux) != 4:
        print 'Bits are over'
        raise ValueError('Bits are over')
    return ''.join(message_aux)

def message_sliced(message):
    message_bin_list = list(convert_message_to_binary(message))
    message_aux = "".join(message_bin_list[0:3])
    message_bin_list = message_bin_list[3:]
    return message_aux


def hide_metadata(size, file_name):
    global LSB_SIZE_BITS
    message_size_bin = convert_decimal_binary(size)
    print message_size_bin
    message_size_bin_padd = add_padding(message_size_bin)
    message_size_bin_padd_list = list(message_size_bin_padd)
    size = dctRed.shape[0]
    line_size = size - 1
    column_size = size - 1
    i=0
    j=0
    while i < line_size:
        while j < column_size:

            if len(message_size_bin_padd_list) > 0:
                binImgR = float_to_bin(dctRed[i][j])
                binImgG = float_to_bin(dctGreen[i][j])
                binImgB = float_to_bin(dctBlue[i][j])
                try:
                    dctRed[i][j] = bin_to_float(binImgR[:-4] + message_size_bin_padd_sliced(message_size_bin_padd_list))
                except:
                    pass
                try:
                    dctGreen[i][j] = bin_to_float(binImgG[:-4] + message_size_bin_padd_sliced(message_size_bin_padd_list))
                except:
                    pass
                try:
                    dctBlue[i][j] = bin_to_float(binImgB[:-4] + message_size_bin_padd_sliced(message_size_bin_padd_list))
                except:
                    pass
                i+=1
                j+=1
            else:
                last = True
                break
        if last == True:
            break

def hide_file(file_name):

    hex = open_file(file_name)
    binary = hex_to_binary(hex)
    message ="sdfssdf"

    global dctRed
    global dctGreen
    global dctBlue

    # print dctRed
    # print "|"
    # print dctGreen
    # print "|"
    # print dctBlue

    #adicionar o padding


    print "File has "+str(len(binary)/8)+" Bytes"
    hide_metadata(len(binary), file_name)

    last_i = 10
    last_j = 0


    size = dctRed.shape[0]
    line_size = size - 1
    column_size = size - 1

    while last_i < line_size:
        while last_i < column_size:

            binImgR = float_to_bin(dctRed[last_i][last_j]) 
            binImgG = float_to_bin(dctGreen[last_i][last_j])
            binImgB = float_to_bin(dctRed[last_i][last_j])
            dctRed[last_i][last_j] = bin_to_float(binImgR[:-4]+message_sliced(message))
            dctGreen[last_i][last_j] = bin_to_float(binImgG[:-4]+message_sliced(message))
            dctBlue[last_i][last_j] = bin_to_float(binImgB[:-4]+message_sliced(message))
            last_i+=1
            last_j+=1
    #
    # print"=========================================================="
    # print dctRed
    # print "|"
    # print dctGreen
    # print "|"
    # print dctBlue
##########################falta fazer o merge das 3 imagens ################ 
#def extract_message(image):


open_image("bg.jpg")
hide_file("LennaS.jpg")






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