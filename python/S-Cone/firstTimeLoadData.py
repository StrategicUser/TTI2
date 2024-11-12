#Should copy gui-data.yml into %PROGRAMDATA%\scone-util\data\, but doesn't always work. Placing file there manually is workaround.

import pathlib
import subprocess

def firstTimeLoadData():

	yamlData= pathlib.Path("/home/strategic/TTI/python/S-Cone/gui-data.yml")

	if yamlData.exists():
		pass
#	else:
#		mkDataFolder = subprocess.call(["cmd", "/c", "mkdir", "C:\\ProgramData\\scone-util\\data"])
#		copy_yaml_data = subprocess.call(["cmd", "/ccopy", ".\gui-data.yml", "C:\\ProgramData\\scone-util\\data"])