#My Glossary Project

from tkinter import *

#key down function

##### main:
window = TK()
window.title("My Computer Science Glossary")
window.configure(background="black")

##### My Photo
photo1 = PhotoImage(file="me.gif")
Label1 (window, image=photo1, bg="black") .grid(row=0, column=0, sticky=W)

#create label
Label (window, text="Enter the words to define:", bg="black", fg=="white", font="none 12 bold") .grid(row=1, column=0, sticky=W)

