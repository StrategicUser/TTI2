import tkinter as tk

class App(tk.Tk):
    
    def __init__(self):
        
        super().__init__()
        self.btn = tk.Button(self, test="Click Me!", command=self.say_helo)
        self.btn.pack(padx=120, pady=30)
        
    def say_hello(self):
        
        print("Hello, Tkinter!")

if __name__ == "__main__":
    app = App()
    app.title("My Tkinter App")
    app.mainloop()