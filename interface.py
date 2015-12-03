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
    LSB.set_image(img)
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
    current_full_size_image.save(fileName.name)



def setImage(img):
    global current_full_size_image
    current_full_size_image = img
    l, h = img.size
    #print l, h
    #print int(250), float(250) / float(l)
    img_resize = img.resize((int(250), int((float(250) / float(l)) * h)), Image.ANTIALIAS)
    #img_resize = img.resize((int(150), int(150)), Image.ANTIALIAS)

    photo = ImageTk.PhotoImage(img_resize)
    label1.configure(image=photo)
    label1.image = photo  # keep a reference!

def donothing():
    filewin = Toplevel(master)
    button = Button(filewin, text="Do nothing button")
    button.pack()

def onOpenFile():
    # Open Callback
    ftypes = [('All Files', '*.jpg')]     #MUDAR ISTO DEPOIS
    dlg = tkFileDialog.Open(filetypes=ftypes)
    filename = dlg.show()
    e1.delete(0,END)
    e1.insert(0,filename)


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

def about_box():
    tkMessageBox.showinfo(title="About", message="Skryvat V1.0\nAuthors:\nFabio Carvalho\nPedro Dias\nCarlos Ribeiro\nIP: Tecnico Lisboa\nRelease: 5 December 2015\nLast Update: 5 December 2015")
    ############################## Interface Code ################################


def intitGui():
    master.title("Welcome and feel free to hide your secrets with us")
    
    #Setting Background
    bg =Image.open('bg2.jpg')
    background_image = ImageTk.PhotoImage(bg)
    w = background_image.width()
    h = background_image.height()
    master.geometry('%dx%d+0+0' % (w,h))
    background_label = Tkinter.Label(master, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image

    ############################## Tool Bar ################################
    menubar = Menu(master)
    master.config(menu=menubar)
    
    ##### EM CASO DE NAO GOSTAREM DAS ALTERACOES #####

    #filemenu.add_command(label="Open", command=onOpen)
    #filemenu.add_command(label="Save as...", command=onSaveAs)
    #filemenu.add_command(label="Close", command=master.quit)
    #filemenu.add_separator()

    #filemenu.add_command(label="Exit", command=master.quit)
    #menubar.add_cascade(label="File", menu=filemenu)
    #editmenu = Menu(menubar, tearoff=0)
    #editmenu.add_command(label="Undo", command=donothing)
    #editmenu.add_separator()

    #editmenu.add_command(label="Cut", command=donothing)
    #editmenu.add_command(label="Copy", command=donothing)
    #editmenu.add_command(label="Paste", command=donothing)
    #editmenu.add_command(label="Delete", command=donothing)
    #editmenu.add_command(label="Select All", command=donothing)
    #menubar.add_cascade(label="Edit", menu=editmenu)

    #helpmenu = Menu(menubar, tearoff=0)
    #helpmenu.add_command(label="Help Index", command=donothing)
    #helpmenu.add_command(label="About...", command=donothing)
    #menubar.add_cascade(label="Help", menu=helpmenu)

    imagemenu = Menu(menubar, tearoff=0)
    imagemenu.add_command(label="Open", command=onOpen)
    imagemenu.add_command(label="Save as...", command=onSaveAs)
    imagemenu.add_separator()
    imagemenu.add_command(label="Replace", command=onOpen)
    menubar.add_cascade(label="Image", menu=imagemenu)

    hidemenu = Menu(menubar, tearoff=0)
    hidemenu.add_command(label="Image", command=onOpen)
    hidemenu.add_command(label="Document", command=onSaveAs)
    hidemenu.add_separator()
    hidemenu.add_command(label="Replace", command=onOpen)
    menubar.add_cascade(label="Hide", menu=hidemenu)

    windowmenu = Menu(menubar, tearoff=0)
    windowmenu.add_command(label="Exit", command=master.quit)
    menubar.add_cascade(label="Window", menu=windowmenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...", command=about_box)
    helpmenu.add_separator()
    helpmenu.add_command(label="Manual", command=donothing)
    menubar.add_cascade(label="Help", menu=helpmenu)


    ################################ Buttons ###########################################

    global label1 
    global e1
    global label2    #To put the result image

    label1 = Tkinter.Label()
    label1.place(relx=.3, rely=.4, anchor="c") 

    label2 = Tkinter.Label()
    label2.place(relx=.7, rely=.4, anchor="c")
    
    button1 = Button(master, text="Select the image", command=onOpen)
    button2 = Button(master, text='Hide your file', command=hide_procedure)
    button3 = Button(master, text='Extract file',  command=extract_message)
    button4 = Button(master, text='Save result', command=onSaveAs)
    button5 = Button(master, text='Choose file to hide', command=onOpenFile)
    e1 = Entry(master)

    button1.place(relx=.3, rely=.6, anchor="c")
    button2.place(relx=.8, rely=.8, anchor="c")    
    button3.place(relx=.8, rely=.9, anchor="c")
    button4.place(relx=.7, rely=.6, anchor="c")
    button5.place(relx=.5, rely=.8, anchor="c")
    e1.place(relx=.5, rely=.9, anchor="c")

    global sb 
    sb = Spinbox(master, values=('Low','Medium','High'))
    sb.place(relx=.2, rely=.83, anchor="c")
    
   
    # ola = convert_message_to_binary("sdfsd")
    #print ola

#if __name__ == "__main__":

startGUI()