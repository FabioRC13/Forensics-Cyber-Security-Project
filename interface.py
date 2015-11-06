#!/usr/bin/python
############################## Imports #########################################
import Tkinter
from Tkinter import *
from tkFileDialog import *
import tkFileDialog
import numpy as np
from PIL import Image,ImageTk

class GUI(Frame):
    def __init__(self):
        self.master = Tk()
        Frame.__init__(self, self.master, background="white")
        self.intitGui()
        self.master.mainloop()


    ############################# Functions ########################################

    def onOpen(self):
        #Open Callback
        ftypes = [('Image Files', '*.tif *.jpg *.png')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        filename = dlg.show()
        self.fn = filename
        #print self.fn #prints filename with path here
        self.setImage()

    def setImage(self):
        self.img = Image.open(self.fn)
        l, h = self.img.size
        print l, h
        print int(250), float(250)/float(l)
        self.img = self.img.resize((int(250), int((float(250)/float(l))*h)), Image.ANTIALIAS)
        #text = str(2*l+100)+"x"+str(h+50)+"+0+0"
        #print text
        #self.master.geometry(text)
        photo = ImageTk.PhotoImage(self.img)
        self.label1.configure(image = photo)
        self.label1.image = photo # keep a reference!

    def donothing(self):
        filewin = Toplevel(self.master)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    ############################## Interface Code ################################

    def intitGui(self):

        self.master.title("Welcome and feel free to hide your secrets with us")
        self.pack()
        #w,h = img.size
        self.master.geometry('%dx%d+0+0' % (500,500))

        self.label1 = Tkinter.Label(self, border = 25)
        self.label1.grid(row = 0, column = 0)

        menubar = Menu(self.master)
        filemenu = Menu(menubar, tearoff=0)
        self.master.config(menu=menubar)

        ############################## Tool Bar ################################
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", command=self.onOpen)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_command(label="Save as...", command=self.donothing)
        filemenu.add_command(label="Close", command=self.donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.donothing)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=self.donothing)
        editmenu.add_command(label="Copy", command=self.donothing)
        editmenu.add_command(label="Paste", command=self.donothing)
        editmenu.add_command(label="Delete", command=self.donothing)
        editmenu.add_command(label="Select All", command=self.donothing)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)
        ############################################################################


        #button1 = Button(self.master, text="Select the image", command=self.search_img)
        e1 = Entry(self.master, text="Write your message")
        button2 = Button(self.master, text='Hide your message')
        #button3 = Button(self.master, text='Exit',  command=self.master.quit)


        button2.grid(row=1)
        button2.pack()
        #button3.grid(row=3)
        #e1.grid(row=4)
