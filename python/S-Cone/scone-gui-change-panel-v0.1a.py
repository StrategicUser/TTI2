##### GUI for customer interaction w/ S-Cone

### Needs



from tkinter import *
from tkinter import ttk
import subprocess
import yaml
import shlex
import os

########
########  LOAD YAML DATA ##############
#######################################

with open('C:\\ProgramData\\scone-util\\data\\gui-data.yml', 'r') as stream:
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

frame = ttk.Labelframe(root, text="S-Cone IP Change", width = 190, height = 690)
frame.grid(column = 0, row = 0)

sconeInfoFrame = ttk.Labelframe(root, text="Current S-Cone IP", width = 301, height = 173, padding = [5, 0, 5, 0])
sconeInfoFrame.grid(column = 0, row = 1)

def launchFTPButton():
	
	def launchFTP():
		DETACHED_PROCESS = 0x00000008
		command = r'cmd /c"C:\Program Files (x86)\WinSCP\WinSCP.exe" ftp://192.168.1.200:1113/ /passive=off'
		#command = r'cmd /c"C:\Program Files (x86)\WinSCP\WinSCP.exe" ftp://speedtest.tele2.net/'
		command_args = shlex.split(command)
		launchFTP = subprocess.Popen(command, creationflags = DETACHED_PROCESS)
	
	goButton = ttk.Button(frame, text="Go", command = launchFTP)
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

def launchBrowserButton():
	
	def launchBrowser():
		command = 'start microsoft-edge:http://' + selectedSconeIp + ':1112'
		command_args = shlex.split(command)
		launchBrowser = subprocess.run(command_args, shell=True)

	goButton = ttk.Button(frame, text="Go", command = launchBrowser)
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

	#if newActionDropdown.get() == 'Ping':

	if newActionDropdown.get() == 'SSH':
		launchSSHButton()
	if newActionDropdown.get() == 'Web':
		launchBrowserButton()
def getSconeIp():
	
	##pull S-Cone Unit IDs and populate S-Cone dropdown

	sconeData = yaml_data['scones']
	
	global selectedSconeIp

	for scone in sconeData:
		if scone == sconeDropdown.get():
			
			currentSconeData = sconeData[scone]
			
			for key in currentSconeData:
				if 'Ip' in key:
					if isListEmpty(selectedSconeIp) == True:
						selectedSconeIp.append(currentSconeData[key])
					if isListEmpty(selectedSconeIp) == False:
						selectedSconeIp = []
						selectedSconeIp.append(currentSconeData[key])
	

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
		else:
			pass

def displaySconeIP():
	
	getSconeIp()
	sconeIpInfo = ttk.Label(sconeInfoFrame, text=selectedSconeIp, padding = [5, 0, 5, 0])
	sconeIpInfo.grid(column = 0, row = 0)

sconeDropdownAndLabel(frame, "S-Cone Name", 0, 1)

b1 = ttk.Button(frame, text="Show IP", command = displaySconeIP)
b1.grid(column=2, row=2)
newIp = StringVar()
newIpLabel = ttk.Label(frame, text="Input New IP")
newIpLabel.grid(column=3, row=1)
e = ttk.Entry(frame, textvariable=newIp)
e.grid(column=3, row=2)
b2 = ttk.Button(frame, text="Change WAN IP", command = launchSSHButton)
b2.grid(column=4, row=2)




root.mainloop()