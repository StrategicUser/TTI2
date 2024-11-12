from tkinter import *
#import tkinter.tkFileDialog

root = Tk()

# Creating a Label Widget
btn = Button(root, text="Click me!")
btn.config(command=lambda: print("Hello, Tkinter!"))
btn.pack(padx=120, pady=30)
root.title("My Tkinter app")

# Putting it on the screen
#mylabel.pack()

root.mainloop()

