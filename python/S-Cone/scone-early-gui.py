##### GUI for customer interaction w/ S-Cone

### Needs

#input S-Cone IP
#navigate to IP:port in iframe?
#have S-Cone ping out - input IP
#Navigate to devices behind S-Cone
#


from tkinter import *
from tkinter import ttk
import subprocess

root = Tk()
root.title('S-Cone Management Utility')
root.geometry("700x275")

frame = ttk.Labelframe(root, text="S-Cone Utility", width = 190, height = 690)
frame.grid(column = 0, row = 0)

pingFrame = ttk.Labelframe(root, text="Ping Results", width = 301, height = 173, padding = [5, 0, 5, 0])
pingFrame.grid(column = 0, row = 1)

def dropdownAndLabel(parent, name, column, row):
	labelColumn = column
	labelRow = row

	dropdown = ttk.Combobox(parent, width = 15, values = ["1", "2", "3"])
	dropdown.grid(column = labelColumn, row = labelRow + 1, padx = 10)

	dropdown.label = ttk.Label(parent, text = name)
	dropdown.label.grid(column = labelColumn, row = labelRow)

def pingClick():
	
	ping = subprocess.run(["ping", "10.0.2.106", "-w", "1", "-n", "2"], capture_output=True, text=True)
	print (ping.stdout)
	pingOutputLabel = ttk.Label(pingFrame, text = ping.stdout)
	pingOutputLabel.grid(column=0, row=0)
	




dropdownAndLabel(frame, "S-Cone Name", 0, 0)

b = ttk.Button(frame, text="Ping S-Cone WAN", command = pingClick)
b.grid(column = 1, row = 1)
b2 = ttk.Button(frame, text="Go")
b2.grid(column=5, row=1)

dropdownAndLabel(frame, "Device", 2, 0)
dropdownAndLabel(frame, "Action", 3, 0)





root.mainloop()