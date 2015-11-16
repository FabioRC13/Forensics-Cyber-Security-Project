#%matplotlib inline
import io
import os
from PIL import Image
import numpy
import numpy
import matplotlib.pyplot as plt
import scipy
from scipy import fftpack
import urllib2
import IPython
import struct


def open_image():
    image = Image.open("LennaS.jpg")
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

pixels = open_image()
print pixels
dct_size = pixels.shape[0]
dct = get_2D_dct(pixels)
print dct
print type(dct[0][0])
print dct[0][4]

print ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', dct[0][0]))
reconstructed_images = []
print dct_size
# Reconstructed image
idct = get_2d_idct(dct)
reconstructed_image = get_reconstructed_image(idct)
reconstructed_image.save("img.png")


print numpy.array(reconstructed_image, dtype=numpy.float)