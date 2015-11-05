from PIL import Image
import six
import binascii

message = "string"

#Create a new image
img = Image.open('photo.png') 

#Create the pixel map
pixels = img.load() 

 # Convert message converted into bits
def convert_message_to_binnary(message):
    result = []
    for c in message:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])

    resaux = ''

    for c in result:
    	caux = str(c)
    	resaux  = resaux + caux + ''

    return resaux

#Convert a decimal number to binnary

def convert_decimal_binnary(value):
    if value == 0: return "0"
    s = ''
    while value:
        if value & 1 == 1:
            s = "1" + s
        else:
            s = "0" + s
        value /= 2
    return s

#Convert bits to text

def convert_bits_text(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int_to_bytes(n).decode(encoding, errors)

#Auxiliar method of the method convert_bits_text

def int_to_bytes(value):
    hex_string = '%x' % value
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

# Method to get the last bit

def get_last_bit(binnarynumber):

    index=0
    binnarynumbersize = (len(binnarynumber))
    lastbit = ''
    while(index < binnarynumbersize-1):
        index = index + 1
   
    lastbit = lastbit + lastbit.join(binnarynumber[index])

    return lastbit



#Replace the last bit of RGB for a bit of the encypted message

def replaceBit(messageConverted, bitposition):

    index=0
    bitpositionsize = (len(bitposition))
    newbit = " "

    while(index < bitpositionsize):
        
        if  index != bitpositionsize-1:
            
           newbit = newbit + newbit.join(bitposition[index])
        else:
            
            newbit = newbit + newbit.join(messageConverted[0])

        index = index + 1

    messageConverted = messageConverted[1:]
    print newbit
    return newbit


#Hide the message in the image

def hide_message(img, message):

    messageConverted = convert_message_to_binnary(message)
    valueBinaryPosition = " "

    for i in range(img.size[0]):
        for j in range(img.size[1]):

            if len(messageConverted) > 0:
                rgbValue = img.getpixel((i,j))
                redValue = convert_decimal_binnary(rgbValue[0])
                greenValue = convert_decimal_binnary(rgbValue[1])
                blueValue = convert_decimal_binnary(rgbValue[2])
                replaceBit(messageConverted, redValue)
                replaceBit(messageConverted, greenValue)
                replaceBit(messageConverted,  blueValue)
            


#Extract the message from the image

def extract_message(img):

    extracted_binnary_message = ''

    for i in range(img.size[0]):
        for j in range(img.size[1]):

            rgbValue = img.getpixel((i,j))
            redValue = convert_decimal_binnary(rgbValue[0])
            greenValue = convert_decimal_binnary(rgbValue[1])
            blueValue = convert_decimal_binnary(rgbValue[2])
            extracted_binnary_message = get_last_bit(redValue) + get_last_bit(greenValue) + get_last_bit(blueValue)

    convert_bits_text(extracted_binnary_message)
    return convert_bits_text


    
#hide_message(img, pixels, "Labyad")
#extract_message(img)
pix="A tua mae de 4"
#replaceBit(pix, "01")
#replaceBit(pix, "01")

yolo = convert_message_to_binnary(pix)
print len(yolo)

ze = convert_bits_text(yolo)
print ze
#img.show()























