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
from subprocess import check_output, PIPE
import yaml
import shlex
import os
from firstTimeLoadData import firstTimeLoadData

########
########  LOAD YAML DATA ##############
#######################################

firstTimeLoadData()
yaml_data_loc = "C:\\ProgramData\\scone-util\\data\\gui-data.yml"


with open(yaml_data_loc, 'r') as stream:
    try:
        yaml_data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

########
######## VARIABLES #########
########
currentSconeData = []
unitIds = yaml_data['scones']
selectedSconeIp = []
selectedDeviceIp = []
selectedDevicePort = []
unitId = []
sconeArray = list(unitIds.keys())
sconeUnitIdArray = []
deviceArray = []
actionArray = []
########
########  GUI ##############
############################

root = Tk()
root.title('S-Cone Management Utility')
root.geometry("700x275")

frame = ttk.Labelframe(root, text="S-Cone Utility", width = 190, height = 690)
frame.grid(column = 0, row = 0)

pingFrame = ttk.Labelframe(root, text="Ping Results", width = 348, height = 173, padding = [10, 0, 10, 0])
pingFrame.grid(column = 0, row = 1)

def launchBrowserButton():
	
	def launchBrowser():
		command = 'start microsoft-edge:http://' + selectedSconeIp + ':' + selectedDevicePort
		command_args = shlex.split(command)
		launchBrowser = subprocess.run(command_args, shell=True)

	goButton = ttk.Button(frame, text="Go", command = launchBrowser)
	goButton.grid(column=5, row=1)

def launchFTPButton():
	
	def launchFTP():
		DETACHED_PROCESS = 0x00000008
		command = r'cmd /c"C:\Program Files (x86)\WinSCP\WinSCP.exe" ftp://192.168.1.200:1113/ /passive=off'
		#command = r'cmd /c"C:\Program Files (x86)\WinSCP\WinSCP.exe" ftp://speedtest.tele2.net/'
		command_args = shlex.split(command)
		launchFTP = subprocess.Popen(command, creationflags = DETACHED_PROCESS)
	
	goButton = ttk.Button(frame, text="Go", command = launchFTP)
	goButton.grid(column=5, row=1)

def launchPingButton():

	def launchPing():
		ping = subprocess.run(["ping", "192.168.2.30", "-w", "1", "-n", "2"], capture_output=True, text=True)
		print (ping.stdout)
		pingOutputLabel = ttk.Label(pingFrame, text = ping.stdout)
		pingOutputLabel.grid(column=0, row=0)

	goButton = ttk.Button(frame, text="Go", command = launchPing)
	goButton.grid(column=5, row=1)

def launchSSHButton():
	
	def launchSSH():
		#command = 'putty.exe -ssh root@' + selectedSconeIp + ' -pw Strategic3!@#$'
		command = 'cmd /cstart putty.exe -ssh root@' + selectedSconeIp + ' -pw Strategic3!@#$'
		command_args = shlex.split(command)
		print(command_args)
		launchSSH = subprocess.run(command)


	goButton = ttk.Button(frame, text="Go", command = launchSSH)
	goButton.grid(column=5, row=1)

def isListEmpty(listOfElements):
	if len(listOfElements) == 0:
		return True
	else:
		return False

def isStrInKeyLoop(key, string):
	print('str')
	if string in key:
		return True
	else:
		return False 

def isStrInList(listOfElements, string):
	if any(string in s for s in listOfElements):
		return True
	else:
		return False

def isFtpInArray():
	if isStrInList(actionArray, 'FTP') is False:
		return False
	else:
		return True

def isSshInArray():
	if isStrInList(actionArray, 'SSH') is False:
		return False
	else:
		return True

def isWebInArray():
	if isStrInList(actionArray, 'Web') is False:
		return False
	else:
		return True

def isPingInArray():
	if isStrInList(actionArray, 'Ping') is False:
		return False
	else:
		return True

def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys

def getSortedSconeUnitIds():
    for value in sconeArray:
        try:
            sconeUnitIdArray.append(value)
        except:
            pass
    sconeUnitIdArray.sort()
getSortedSconeUnitIds()

def getDropdownSelection(event):
	if newActionDropdown.get() == 'FTP':
		launchFTPButton()
	if newActionDropdown.get() == 'Ping':
		launchPingButton()
	if newActionDropdown.get() == 'SSH':
		launchSSHButton()
	if newActionDropdown.get() == 'Web':
		launchBrowserButton()

def getDeviceActions(event):
	print('selected', event.widget.get())

	##pull S-Cone Unit IDs and populate S-Cone dropdown
	
	global actionArray
	actionArray = []  #clear dropdown list data from previous choices
	currentSconeData = yaml_data['scones'][sconeDropdown.get()]

	#Add Device actions for selected S-Cone device to action dropdown
	
	for devId in currentSconeData:
		if 'dev' in devId:
			currentSconeDevData = currentSconeData[devId]
			for key in currentSconeDevData:
				if 'Id' in key:
					if currentSconeDevData[key] == event.widget.get():
						for key in currentSconeDevData:
							while 'Ftp' in key and isFtpInArray() == False:
								actionArray.append('FTP')
							while 'Ssh' in key and isSshInArray() == False:
								actionArray.append('SSH')
							while 'Web' in key and isWebInArray() == False:
								actionArray.append('Web')
							#while 'ping' in key and isPingInArray() == False:
								#actionArray.append('Ping')
							else:
								continue
					updatedActionDropdown(frame, "Action", 4, 0, actionArray)
		else:
			pass
	
	#Get Selected Device's IP

	global selectedDeviceIp

	for devId in currentSconeData:
		if 'dev' in devId:
			currentSconeDevData = currentSconeData[devId]
			for key in currentSconeDevData:
				if 'Id' in key:
					if currentSconeDevData[key] == event.widget.get():
						for key in currentSconeDevData:
							if 'Ip' in key:
								if isListEmpty(selectedDeviceIp) == True:
									selectedDeviceIp.append(currentSconeDevData[key])
								if isListEmpty(selectedDeviceIp) == False:
									selectedDeviceIp = []
									selectedDeviceIp.append(currentSconeDevData[key])

	global selectedDevicePort

	for devId in currentSconeData:
		if 'dev' in devId:
			currentSconeDevData = currentSconeData[devId]
			for key in currentSconeDevData:
				if 'Port' in key:
					if 'Forward' in key:
						continue
					selectedDevicePort = str(currentSconeDevData.get(key))					
	
def deviceDropdownAndLabel(parent, name, column, row):
	labelColumn = column
	labelRow = row
	deviceDropdown.grid(column = labelColumn, row = labelRow + 1, padx = 10)
	deviceDropdown.label = ttk.Label(parent, text = name)
	deviceDropdown.label.grid(column = labelColumn, row = labelRow)

def actionDropdownAndLabel(parent, name, column, row):
	labelColumn = column
	labelRow = row
	actionDropdown.grid(column = labelColumn, row = labelRow + 1, padx = 10)
	actionDropdown.label = ttk.Label(parent, text = name)
	actionDropdown.label.grid(column = labelColumn, row = labelRow)


sconeDropdown = ttk.Combobox(frame, width = 15, values = sconeUnitIdArray) 
deviceDropdown = ttk.Combobox(frame, width = 15, values = deviceArray)
actionDropdown = ttk.Combobox(frame, width = 15, values = actionArray)


def sconeDropdownAndLabel(parent, name, column, row):
	
	labelColumn = column
	labelRow = row 
	sconeDropdown.bind("<<ComboboxSelected>>", getSconeDevices)
	sconeDropdown.grid(column = labelColumn, row = labelRow + 1, padx = 10)
	sconeDropdown.label = ttk.Label(parent, text = name)
	sconeDropdown.label.grid(column = labelColumn, row = labelRow)
	

def getSconeDevices(event):
	##pull S-Cone Unit IDs and populate S-Cone dropdown
	deviceArray = []
	loadScone = yaml_data['scones'][sconeDropdown.get()]
	currentSconeData = loadScone
	global selectedSconeId
	global selectedSconeIp
	selectedSconeId = yaml_data['scones'][sconeDropdown.get()]
	selectedSconeIp = yaml_data['scones'][sconeDropdown.get()]['sconeIp']
	#pull Device names for selected S-Cone Unit ID

	for devId in currentSconeData:
		if 'dev' in devId:
			currentSconeDevData = currentSconeData[devId]
			for key in currentSconeDevData:
				if 'Id' in key:
					deviceArray.append(currentSconeDevData[key])
					updatedDeviceDropdown(frame, "Device", 3, 0, deviceArray)
		else:
			pass

#class dependentDropdown(ttk.Combobox):
#
#	def __init__(self, parent, name, column, row, values):
#		self.parent = parent
#		self.label = ttk.Label(parent, text = name)
#		self.values = values
#		self.label.grid(column = column, row = row)
#		self.grid(column = column, row = row + 1, padx = 10)


def updatedDeviceDropdown(parent, name, column, row, values):
	labelColumn = column
	labelRow = row
	dropdown = ttk.Combobox(parent, width = 15, values = values)
	dropdown.bind("<<ComboboxSelected>>", getDeviceActions)
	dropdown.grid(column = labelColumn, row = labelRow + 1, padx = 10)
	dropdown.label = ttk.Label(parent, text = name)
	dropdown.label.grid(column = labelColumn, row = labelRow)

def updatedActionDropdown(parent, name, column, row, values):
	labelColumn = column
	labelRow = row
	global newActionDropdown
	newActionDropdown = ttk.Combobox(parent, width = 15, values = values)
	newActionDropdown.bind("<<ComboboxSelected>>", getDropdownSelection)
	newActionDropdown.grid(column = labelColumn, row = labelRow + 1, padx = 10)
	newActionDropdown.label = ttk.Label(parent, text = name)
	newActionDropdown.label.grid(column = labelColumn, row = labelRow)
	
def pingClickScone():

	#runPing = open (.\)
	

	command = r'cmd /c ping ' + selectedSconeIp + r' -w 1 -n 2 > C:\\ProgramData\\scone-util\\ping'
	command_args = shlex.split(command)
	ping = subprocess.run(command_args)
	


	openOutput = open("C:\\ProgramData\\scone-util\\ping", "r")
	output = openOutput.read()
	pingOutputLabel = ttk.Label(pingFrame, text = output, padding = [10, 0, 10, 0])
	pingOutputLabel.grid(column=0, row=0)
	openOutput.close()
	

def launchSconeGui():
	
	command = 'start microsoft-edge:http://' + selectedSconeIp + ':20080'
	#ommand_args = shlex.split(command)
	#print(command_args)
	ping = subprocess.run(["ping", selectedSconeIp, "-w", "1", "-n", "2"], capture_output=True, text=True)
	pingOutputLabel = ttk.Label(pingFrame, text = ping.stdout)
	pingOutputLabel.grid(column=0, row=0)

def pingClickDevice():
	
	ping = subprocess.run(["ping", selectedSconeIp, "-w", "1", "-n", "2"], capture_output = True, shell = True)
	#print (ping.stdout)
	output = ping
	check = check_output(output)
	print (check)
	face = 'facce'
	pingOutputLabel = ttk.Label(pingFrame, text = face)
	pingOutputLabel.grid(column=0, row=0)

def launchSSH():
		#command = 'putty.exe -ssh root@' + selectedSconeIp + ' -pw Strategic3!@#$'
		command = 'cmd /cstart putty.exe -ssh root@' + selectedSconeIp + ' -pw Strategic3!@#$'
		command_args = shlex.split(command)
		print(command_args)
		launchSSH = subprocess.run(command)

#def takeAction():
#	if

#dropDown = loadSconeDataAndEnableDeviceDropdown()

#testEnable = dropdownState(dropDown)

sconeDropdownAndLabel(frame, "S-Cone Name", 0, 0)
deviceDropdownAndLabel(frame, "Device", 3, 0)
actionDropdownAndLabel(frame, "Action", 4, 0)

pingWanButton = ttk.Button(frame, text="Ping S-Cone WAN", command = pingClickScone)
pingWanButton.grid(column = 1, row = 1)
launchSconeGui = ttk.Button(frame, text="Launch S-Cone GUI", command = pingClickScone)

sshWanButton = ttk.Button(frame, text="SSH to S-Cone", command = launchSSH)
sshWanButton.grid(column = 2, row = 1)
goButton = ttk.Button(frame, text="Go", state = 'disabled')
goButton.grid(column=5, row=1)

root.mainloop()