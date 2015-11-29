import binascii

def open_file(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    return binascii.hexlify(content)

def save_file(filename, hex):
    file = open(filename, "wb")
    newfile = binascii.unhexlify(hex)
    file.write(newfile)
    file.close()

filename = "ccsetup512.exe"
hex = open_file(filename)
print hex
save_file("a"+filename, hex)