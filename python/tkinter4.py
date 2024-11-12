from tkinter import *

root = Tk()
btn = Button(root, test="Click Me!")
btn.config(command=lambda: print("Hello, Tkinter!"))
btn.pack(padx=120, pady=30)
root.title("My Tkinter App")
root.mainloop()
