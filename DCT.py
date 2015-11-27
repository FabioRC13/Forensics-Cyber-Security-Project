#%matplotlib inline
import io
import os
from PIL import Image
import numpy
import matplotlib.pyplot as plt
import scipy
from scipy import fftpack
import urllib2
#import IPython
import struct

message = "Bailando"


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


def open_image():
    image = Image.open("LennaS.jpg").convert('RGB')
    image.save("original.png")
    r, g, b = image.split()
    r.save("imgR.png")
    b.save("imgB.png")
    g.save("imgG.png")
    out = Image.merge("RGB", (r, g, b))
    out.save("merged.png")
    #print numpy.array(r, dtype=numpy.float)
    #img_color = image.resize(size, 1)
    img_grey = image.convert('L')
    img = numpy.array(img_grey, dtype=numpy.float)
    return img

def get_2D_dct(img):
    """ Get 2D Cosine Transform of Image
    """
    return fftpack.dct(fftpack.dct(img.T, norm='ortho').T, norm='ortho')

def get_2d_idct(coefficients):
    """ Get 2D Inverse Cosine Transform of Image
    """
    return fftpack.idct(fftpack.idct(coefficients.T, norm='ortho').T, norm='ortho')

def get_reconstructed_image(raw):
    img = raw.clip(0, 255)
    img = img.astype('uint8')
    img = Image.fromarray(img)
    return img

#converte o float64 num inteiro 
def convert_float64_int(dct):
   return dct.astype(numpy.int64)

#converte o inteiro num float64
def convert_int_float64(inteiro):
    return inteiro.astype(numpy.float64)
    
#message_bits = convert_message_to_binary(message)

pixels = open_image()
print pixels
dct_size = pixels.shape[0]
dct = get_2D_dct(pixels)
print dct

#Para entender o que e um coeficiente DCT
#print type(dct[0][0])

res = convert_float64_int(dct[0][0])

print res

print convert_int_float64(res)

print res == convert_int_float64(res)
#converte para binario (mas apenas mostra 32bits, e o tipo supostamente e  'numpy.float64')
#print ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', dct[0][0]))
#for i in range (0, dct_size):
    #dct[i][i] = 0

#print dct_size
# Reconstructed image
idct = get_2d_idct(dct)
reconstructed_image = get_reconstructed_image(idct)
reconstructed_image.save("img.png")


print numpy.array(reconstructed_image, dtype=numpy.float)