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
yaml_data_loc = "/home/strategic/TTI/python/S-Cone/gui-data.yml"


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

