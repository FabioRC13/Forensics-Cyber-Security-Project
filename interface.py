#!/usr/bin/python
############################## Imports #########################################
import Tkinter
from Tkinter import *
from tkFileDialog import *
from PIL import Image,ImageTk

############################# Functions ########################################
def search_img():
	name_img = askopenfilename()
	print name_img

def donothing():
   filewin = Toplevel(master)
   button = Button(filewin, text="Do nothing button")
   button.pack()
############################## Interface Code ################################

master = Tk()
master.title("Welcome and feel free to hide your secrets with us")

img = Image.open('bg.jpg')
tkimage = ImageTk.PhotoImage(img)
background = Tkinter.Label(master,image = tkimage)
background.place(x=0, y=0, relwidth=1, relheight=1)
w,h = img.size
master.geometry('%dx%d+0+0' % (w,h))

menubar = Menu(master)
filemenu = Menu(menubar, tearoff=0)

filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=search_img)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)

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

button1 = Button(master, text="Select the image", command=search_img)
button1.place(relx=0.5, rely=0.5, anchor=CENTER)

e1 = Entry(master, text="Write your message")
e1.place(relx=0.5, rely=0.6, anchor=CENTER)


button2 = Button(master, text='Hide your message')
button2.place(relx=0.7, rely=0.6, anchor=CENTER)

button3 = Button(master, text='Exit',  command=master.quit)
button3.place(relx=0.8, rely=0.8, anchor=CENTER)

master.config(menu=menubar)
master.mainloop()



	
