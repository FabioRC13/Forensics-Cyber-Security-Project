#!/usr/bin/python
############################## Imports #########################################
import Tkinter
from Tkinter import *
from tkFileDialog import *
import tkFileDialog
import tkMessageBox
import numpy as np
from PIL import Image, ImageTk
import LSB

current_full_size_image = None

def startGUI():
    global master
    master = Tk()
    intitGui()
    master.mainloop()
    ############################# Functions ########################################


def onOpen():
    # Open Callback
    ftypes = [('Image Files', '*.tif *.jpg *.png')]
    dlg = tkFileDialog.Open(filetypes=ftypes)
    filename = dlg.show()
    fn = filename
    #print fn #prints filename with path here
    img = Image.open(fn)
    setImage(img)

def onSaveAs():
    ftypes = [
    ('Windows Bitmap','*.bmp'),
    ('Portable Network Graphics','*.png'),
    ('JPEG / JFIF','*.jpg'),
    ('CompuServer GIF','*.gif'),
    ]
    fileName = tkFileDialog.asksaveasfile(parent=master,filetypes=ftypes ,title="Save the image as...", mode='w',defaultextension='.jpg')
    global current_full_size_image
    print fileName.name
    current_full_size_image.save(fileName.name, quality=100)



def setImage(img):
    global current_full_size_image
    current_full_size_image = img
    l, h = img.size
    #print l, h
    #print int(250), float(250) / float(l)
    img_resize = img.resize((int(250), int((float(250) / float(l)) * h)), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img_resize)
    label1.configure(image=photo)
    label1.image = photo  # keep a reference!

def donothing():
    filewin = Toplevel(master)
    button = Button(filewin, text="Do nothing button")
    button.pack()

def dialog_box(msg):
    tkMessageBox.showwarning("Warning", msg)

def hide_procedure():
    global current_full_size_image
    message = e1.get()
    if message == "":
        dialog_box("Please write your message")
        return
    #if current_full_size_image equal None:
        #dialog_box("No image selected")
        #return

    print e1.get()
    LSB.hide_message(current_full_size_image, e1.get())
    dialog_box("DONE")
    setImage(LSB.img)

def extract_message():
    global current_full_size_image
    message = LSB.extract_message(current_full_size_image)
    print message
    dialog_box(message)

    ############################## Interface Code ################################


def intitGui():
    master.title("Welcome and feel free to hide your secrets with us")
    # pack()
    #w,h = img.size
    master.geometry('%dx%d+0+0' % (300,400))

    global label1 #e global para poder ser acedida noutas funcoes
    global e1

    label1 = Tkinter.Label(border=25)
    #label1.grid(row = 0, column = 0)
    label1.grid(row=0)
    menubar = Menu(master)
    filemenu = Menu(menubar, tearoff=0)
    master.config(menu=menubar)

    ############################## Tool Bar ################################
    #filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=onOpen)
    #filemenu.add_command(label="Save", command=donothing)
    filemenu.add_command(label="Save as...", command=onSaveAs)
    filemenu.add_command(label="Close", command=master.quit)
    filemenu.add_separator()

    filemenu.add_command(label="Exit", command=master.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Undo", command=donothing)
    editmenu.add_separator()

    editmenu.add_command(label="Cut", command=donothing)
    editmenu.add_command(label="Copy", command=donothing)
    editmenu.add_command(label="Paste", command=donothing)
    editmenu.add_command(label="Delete", command=donothing)
    editmenu.add_command(label="Select All", command=donothing)
    menubar.add_cascade(label="Edit", menu=editmenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    menubar.add_cascade(label="Help", menu=helpmenu)
    ############################################################################


    #button1 = Button(master, text="Select the image", command=search_img)
    e1 = Entry(master, text="Write your message")
    button2 = Button(master, text='Hide your message', command=hide_procedure)
    button3 = Button(master, text='Extract message',  command=extract_message)


    #button2.grid(row=1)
    button2.grid(row=1)
    e1.grid(row=2)
    button3.grid(row=3)
    #e1.grid(row=4)

    # ola = convert_message_to_binary("sdfsd")
    #print ola

#if __name__ == "__main__":

startGUI()