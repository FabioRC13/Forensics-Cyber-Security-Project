from PIL import Image
import six
import binascii



# Create a new image
img = Image.open('Lenna.jpg')

# Create the pixel map
pixels = img.load()

# Convert message  into bits
def convert_message_to_binary(message):
    result = ''
    for c in message:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result = result + bits
    return result


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

def utf8_to_bin(text):
    return '{:b}'.format(int(text.encode('utf-8').encode('hex'), 16))


def bin_to_utf8(bits):
    ('%x' % int(bits, 2)).decode('hex').decode('utf-8')

#Convert bits to text

def convert_bits_text(bits, encoding='utf-8', errors='surrogatepass'):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


#Auxiliar method of the method convert_bits_text

def int_to_bytes(value):
    hex_string = '%x' % value
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


# Method to get the last bit

def get_last_bit(binarynumber):
    lastbit = len(binarynumber) - 1

    return binarynumber[lastbit]


#Replace the last bit of RGB for a bit of the encypted message

def replaceBit(messageConverted, bitposition):
    index = 0
    bitpositionsize = (len(bitposition))
    newbit = " "

    while (index < bitpositionsize):

        if index != bitpositionsize - 1:

            newbit = newbit + newbit.join(bitposition[index])

        else:

            newbit = newbit + newbit.join(messageConverted[0])

        index = index + 1

    return newbit


# Hide the size of message in the first pixel
def hide_size(message):
    messagesize = len(message)
    global messagesizeinbits
    messagesizeinbits = convert_decimal_binary(messagesize)

    rgbValue = pixels[0, 0]
    """Um tupulo e um tipo imutaveis por isso tem de ser convertido numa lista por forma a ser manipulado"""

    rgbValue = list(rgbValue)

    blueValue = messagesizeinbits[0:8]
    greenValue = messagesizeinbits[8:16]
    redValue = messagesizeinbits[16:24]

    rgbValue[2] = int(blueValue, 2)

    if greenValue != '':
        rgbValue[1] = int(greenValue, 2)
    else:
        rgbValue[1] = 0

    if redValue != '':
        rgbValue[0] = int(redValue, 2)
    else:
        rgbValue[0] = 0

    rgbValue = tuple(rgbValue)
    pixels[0, 0] = rgbValue


def get_hide_size(pixels):
    rgbValue = pixels[0, 0]

    redValue = convert_decimal_binary(rgbValue[0])
    greenValue = convert_decimal_binary(rgbValue[1])
    blueValue = convert_decimal_binary(rgbValue[2])

    sizeBits = redValue + greenValue + blueValue + ''
    sizeInt = int(sizeBits, 2)
    return sizeInt


#Hide the message in the image

def hide_message(img, message):
    messageConverted = convert_message_to_binary(message)
    #print message
    #print messageConverted
    size = len(messageConverted)
    #print size
    #print "======================"

    hide_size(message)

    for i in range(img.size[0]):
        for j in range(img.size[1]):

            if i == 0 and j == 0:
                continue

            if len(messageConverted) > 0:

                rgbValue = pixels[i, j]
                #print messageConverted
                redValue = convert_decimal_binary(rgbValue[0])
                greenValue = convert_decimal_binary(rgbValue[1])
                blueValue = convert_decimal_binary(rgbValue[2])

                #print pixels[i,j], redValue, greenValue, blueValue

                if len(messageConverted) > 0:
                    redValue = replaceBit(messageConverted, redValue)
                    messageConverted = update(messageConverted)

                if len(messageConverted) > 0:
                    greenValue = replaceBit(messageConverted, greenValue)
                    messageConverted = update(messageConverted)

                if len(messageConverted) > 0:
                    blueValue = replaceBit(messageConverted, blueValue)
                    messageConverted = update(messageConverted)

                #print "(",int(redValue,2),",", int(greenValue,2), ",",int(blueValue,2), ")",  redValue, greenValue, blueValue
                redValue = int(redValue, 2)
                greenValue = int(greenValue, 2)
                blueValue = int(blueValue, 2)

                pixels[i, j] = (redValue, greenValue, blueValue)


                #print "==========================="


#Update the converted message
def update(messageConverted):
    return messageConverted[1:]


#Extract the message from the image
def extract_message(img):
    pixels = img.load()

    messagesize = get_hide_size(pixels)
    extracted_binary_message = ''
    #print messagesize

    end = False
    for i in range(img.size[0]):
        for j in range(img.size[1]):

            if i == 0 and j == 0:
                continue

            rgbValue = pixels[i, j]
            redValue = convert_decimal_binary(rgbValue[0])
            greenValue = convert_decimal_binary(rgbValue[1])
            blueValue = convert_decimal_binary(rgbValue[2])
            extracted_binary_message = extracted_binary_message + get_last_bit(redValue) + get_last_bit(
                greenValue) + get_last_bit(blueValue)
            #print extracted_binary_message
            if len(extracted_binary_message) > messagesize * 8:
                end = True
                break
        if end:
            break

    message = convert_bits_text(extracted_binary_message)

    return message

###### TESTES ########
#largeutf8string = "Convert text into ASCII number format. For example A is 065. Text in a computer is stored as numbers called ASCII numbers with each letter having its own number. Input text to convert to these ASCII numbers. ASCII is short for American Standard Code for Information Interchange. With applications in computers and other devices that use text, ASCII codes represent text. Based on the English alphabet, ASCII is a character-encoding scheme. ASCII was originally developed from telegraphic codes.Computers can only understand numbers, and ASCII codes are numerical representations of characters that a computer can understand. Examples of characters are a, 1, or >. For example, 097 is the ASCII numerical representation of the character a. ASCII covers over 100 characters with some of these characters being control characters that control how text appears.Work on ASCII began in the 1960s through a committee of the American Standards Association. Many of todays character-encoding schemes are based on ASCII, plus they include additional characters. At one time ASCII was used on the World Wide Web as the most commonly used character encoding. If you prepare a text in ASCII format, you will get plain text with no format such as bold, and any computer can understand the format. Other schemes such as HTML cover formatting."
#samllString = "temos de ter uma mensagem enorme para poder realmente verificar se esta a aconntecer alguma coisa com a imagem. nao se pode ter uma frase ou duas :D"

#hide_message(img, samllString)
#print extract_message(img)

#var = utf8_to_bin(samllString)
#print var

#tamanho = "temos de ter uma mensagem enorme para poder realmente verificar se esta a aconntecer alguma coisa com a imagem. nao se pode ter uma frase ou duas :D"
#print get_hide_size("101010101011101")
#img.show()















