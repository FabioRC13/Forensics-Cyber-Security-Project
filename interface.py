#!/usr/bin/python
############################## Imports #########################################
import Tkinter
from Tkinter import *
from tkFileDialog import *
import tkFileDialog
import tkMessageBox
import numpy as np
from PIL import Image, ImageTk
import LSBv2

current_full_size_image = None
current_recoverd_file = None
filename = ""
sb = None

def startGUI():
    global master
    master = Tk()
    intitGui()
    master.mainloop()
############################# Functions ########################################


def onOpen():
    global filename
    # Open Callback
    ftypes = [('Image Files', '*.tif *.jpg *.png')]
    dlg = tkFileDialog.Open(filetypes=ftypes)
    filename = dlg.show()

    if filename != None:
        print filename
        img = Image.open(filename)
        setImage(img,1)
        lsb = setQuality()
        LSBv2.open_image(filename,lsb)
        onSpinboxChanged()


def onSaveAs():
    ftypes = [
    ('Windows Bitmap','*.bmp'),
    ('Portable Network Graphics','*.png'),
    ('JPEG / JFIF','*.jpg'),
    ('CompuServer GIF','*.gif'),
    ]
    fileName = tkFileDialog.asksaveasfile(parent=master,filetypes=ftypes ,title="Save the image as...", mode='w',defaultextension='.jpg')
    global current_full_size_image
    #print fileName.name
    if fileName != None:
        current_full_size_image.save(fileName.name)



def setImage(img, label):
    global current_full_size_image
    current_full_size_image = img

    l,h = img.size
    img_resize = img.resize((int(150), int((float(150) / float(l)) * h)), Image.ANTIALIAS)
   
    if label == 1: 
    	photo = ImageTk.PhotoImage(img_resize)
    	label1.configure(image=photo)
    	label1.image = photo  # keep a reference!
    elif label == 2: 
    	photo = ImageTk.PhotoImage(img_resize)
    	label2.configure(image=photo)
    	label2.image = photo  # keep a reference!


def onOpenFile():
    # Open Callback 
    global filename
    global e2
    
    dlg = tkFileDialog.Open()
    filename = dlg.show()
    e2.delete(0,END)
    e2.insert(0,filename)
    return filename


def dialog_box(msg):
    tkMessageBox.showwarning("Warning", msg)

def hide_procedure():

    if filename == "":
        dialog_box("Please choose a file")
        return

    lsb = setQuality()

    try:
        hide_img = LSBv2.hide_file(filename, int(lsb))
    except ValueError as e:
        dialog_box(e)
        return

    dialog_box("DONE")
    setImage(hide_img,2)


def extract_message():
    global filename
    try:
        newFile, file_name = LSBv2.extract(filename)
        fileName = tkFileDialog.asksaveasfile(parent=master, initialfile=file_name, title="Save the image as...", mode='w')
        #print fileName.name
        if fileName != None:
            LSBv2.save_file(fileName.name, newFile)
    except:
        dialog_box("Invalid file selected")
        return
    print file_name



def setQuality():
    global e1
    quality_value = sb.get()
    if quality_value=="Low":
    	lsb = 1
        #e1.insert("Available size = " + str(DCT.get_image_theoretical_max_available_size(lsb)/8) + " KBytes")
    elif quality_value=="Medium":
    	lsb = 2
    elif quality_value=="High":
    	lsb = 3
    elif quality_value=="Insane":
    	lsb = 6

    return lsb

def onSpinboxChanged(event = None):
    global e1
    e1.delete(0,END)
    quality_value = sb.get()
    lsb = setQuality()
    try:
        e1.insert(0,"Available size = " + str(LSBv2.get_image_theoretical_max_available_size(lsb)/1024.0) + " KBytes")
    except:
        pass

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
    helpmenu.add_command(label="Manual")
    menubar.add_cascade(label="Help", menu=helpmenu)


    ################################ Buttons ###########################################

    global label1 
    global e1
    global label2    #To put the result image
    global e2

    label1 = Tkinter.Label()
    label1.place(relx=.3, rely=.4, anchor="c") 

    label2 = Tkinter.Label()
    label2.place(relx=.7, rely=.4, anchor="c")

    
    button1 = Button(master, text="Select the image", border=0, command=onOpen)
    button2 = Button(master, text='Hide your file', border=0, command=hide_procedure)
    button3 = Button(master, text='Extract file',  border=0, command=extract_message)
    button4 = Button(master, text='Save result', border=0,command=onSaveAs)
    button5 = Button(master, text='Choose file to hide', border=0, command=onOpenFile)
    e1 = Entry(master, width=34)
    e2 = Entry(master)

    button1.place(relx=.3, rely=.6, anchor="c")
    button2.place(relx=.8, rely=.8, anchor="c")    
    button3.place(relx=.8, rely=.9, anchor="c")
    button4.place(relx=.7, rely=.6, anchor="c")
    button5.place(relx=.5, rely=.8, anchor="c")
    e1.place(relx=.2, rely=.9, anchor="c")
    e2.place(relx=.5, rely=.9, anchor="c")

    #e1.delete(0,END)
    #e1.insert(0,"sdf")


    global sb 
    sb = Spinbox(master, border=0, values=('Low','Medium','High','Insane'), command=onSpinboxChanged)
    sb.place(relx=.2, rely=.83, anchor="c")

   
    # ola = convert_message_to_binary("sdfsd")
    #print ola

#if __name__ == "__main__":

startGUI()