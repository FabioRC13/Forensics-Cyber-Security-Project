import binascii
import os

current_file_size_bytes = 0



def open_file(filename):
    global current_file_size_bytes
    with open(filename, 'rb') as f:
        content = f.read()
    st = os.stat(filename)
    current_file_size_bytes = st.st_size
    return binascii.hexlify(content)

def save_file_from_hex(filename, hex):
    file = open(filename, "wb")
    newfile = binascii.unhexlify(hex)
    file.write(newfile)
    file.close()

def save_file(filename, fileContent):
    file = open(filename, "wb")
    file.write(fileContent)
    file.close()

def hex_to_binary(h):
    return ''.join(byte_to_binary(ord(b)) for b in binascii.unhexlify(h))

def byte_to_binary(n):
    return ''.join(str((n & (1 << i)) and 1) for i in reversed(range(8)))

def convert_bits_text(bits, encoding='utf-8', errors='surrogatepass'):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

filename = "ccsetup512.exe"
hex = open_file(filename)
print current_file_size_bytes
print "DONE-1"
# binary = hex_to_binary(hex)
# print "DONE-2"
# newfile = convert_bits_text(binary)
# print "DONE-3"
# save_file("a"+filename, newfile)
# print "DONE-4"