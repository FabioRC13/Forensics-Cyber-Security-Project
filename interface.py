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


############################## Interface Code ################################

master = Tk()
master.title("Welcome and feel free to hide your secrets with us")

img = Image.open('bg.jpg')
tkimage = ImageTk.PhotoImage(img)
background = Tkinter.Label(master,image = tkimage)
background.place(x=0, y=0, relwidth=1, relheight=1)
w,h = img.size
master.geometry('%dx%d+0+0' % (w,h))


button1 = Button(master, text="Select the image", command=search_img)
button1.place(relx=0.5, rely=0.5, anchor=CENTER)

e1 = Entry(master, text="Write your message")
e1.place(relx=0.5, rely=0.6, anchor=CENTER)


button2 = Button(master, text='Hide your message')
button2.place(relx=0.7, rely=0.6, anchor=CENTER)

button3 = Button(master, text='Exit',  command=master.quit)
button3.place(relx=0.8, rely=0.8, anchor=CENTER)

master.mainloop()



	
