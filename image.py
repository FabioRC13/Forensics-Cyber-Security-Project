from PIL import Image
import six
import binascii


#Create a new image
img = Image.open('photo.png') 

#Create the pixel map
pixels = img.load() 

 # Convert message  into bits
def convert_message_to_binary(message):
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

def get_last_bit(binarynumber):

   	lastbit = len(binarynumber)-1

	return binarynumber[lastbit]

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
   
    return newbit

# Hide the size of message in the first 10 pixels
def hide_size(img, size):
 
    for i in range(10):
        for j in range(10):

            if len(messageConverted) > 0:

                rgbValue = pixels[i,j]
                redValue = convert_decimal_binary(rgbValue[0])
                greenValue = convert_decimal_binary(rgbValue[1])
                blueValue = convert_decimal_binary(rgbValue[2])

                if len(messageConverted) > 0:
                	redValue = replaceBit(messageConverted, redValue) 
                	messageConverted = update(messageConverted)

                elif len(messageConverted) > 0:
                	greenValue = replaceBit(messageConverted, greenValue) 
                	messageConverted = update(messageConverted)

                elif len(messageConverted) > 0:
                	blueValue = replaceBit(messageConverted,  blueValue) 
               		messageConverted = update(messageConverted)


               	redValue = int(redValue,2)
                greenValue = int(greenValue,2)
                blueValue = int(blueValue,2)

            	pixels[i, j] = (redValue, greenValue, blueValue)

#Hide the message in the image

def hide_message(img, message):

    messageConverted = convert_message_to_binary(message)
    size = len(messageConverted)

    binSize = convert_decimal_binary(size)


    # We reserve the first 10*10 pixels to hide the message size
    for i in range(10,img.size[0]):
        for j in range(10,img.size[1]):

            if len(messageConverted) > 0:

                rgbValue = pixels[i,j]
                redValue = convert_decimal_binary(rgbValue[0])
                greenValue = convert_decimal_binary(rgbValue[1])
                blueValue = convert_decimal_binary(rgbValue[2])

                if len(messageConverted) > 0:
                	redValue = replaceBit(messageConverted, redValue) 
                	messageConverted = update(messageConverted)

                elif len(messageConverted) > 0:
                	greenValue = replaceBit(messageConverted, greenValue) 
                	messageConverted = update(messageConverted)

                elif len(messageConverted) > 0:
                	blueValue = replaceBit(messageConverted,  blueValue) 
               		messageConverted = update(messageConverted)


               	redValue = int(redValue,2)
                greenValue = int(greenValue,2)
                blueValue = int(blueValue,2)

            	pixels[i, j] = (redValue, greenValue, blueValue)


#Update the converted message
def update(messageConverted):

	return messageConverted[1:]


#Extract the message from the image

def extract_message(img):

    extracted_binary_message = ''

    # We reserve the first 10*10 pixels to hide the message size and search our message until hide size
    for i in range(10,size):
        for j in range(10,size):

            rgbValue = pixels[i,j]
            redValue = convert_decimal_binary(rgbValue[0])
            greenValue = convert_decimal_binary(rgbValue[1])
            blueValue = convert_decimal_binary(rgbValue[2])
            extracted_binary_message = get_last_bit(redValue) + get_last_bit(greenValue) + get_last_bit(blueValue)

    message = convert_bits_text(extracted_binary_message)

    return message


    
###### TESTES ########
""" hide_message(img, "temos de ter uma mensagem enorme para poder realmente verificar se esta a aconntecer alguma coisa com a imagem. nao se pode ter uma frase ou duas :D")

print extract_message(img)


img.show() """ 



















