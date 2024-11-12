import paramiko
import telnetlib
import getpass
import re

#database or summary; used in portchannel
command = 'database'
path_platform = "files/hardwarePlatform.txt"
path_mac_config = "files/mac_config.txt"

#################### SSH ####################
def ssh_exec_command(ssh_obj, command, splitLines=False):
    """execute ssh command"""
    stdin, stdout, stderr = ssh_obj.exec_command(command)
    output = stdout.read().decode()
    if splitLines:
        return output.splitlines(True)
    else:
        return output

################## telnet ###################
def telnet_read(telnet_obj, expected, timeout=None):
    output = telnet_obj.read_until(expected.encode(), timeout).decode()
    return output

def telnet_write(telnet_obj, string, isCommand=True):
    telnet_obj.write(string.encode() + b'\n')
    if isCommand:
        telnet_read(telnet_obj, string)

def login(obj, username, password):
    """login via telnet"""
    telnetIsOpen = True
    count = 0
    while telnetIsOpen:
        #username
        telnet_read(obj, "Username: ")
        telnet_write(obj, username, False)
        #password
        telnet_read(obj, "Password: ")
        telnet_write(obj, password, False)
        #prompt
        response = telnet_read(obj, "#", 2)
        if response != '':
            hostname = response
            break
        if count == 2:
            telnetIsOpen = False
            hostname = ''
            print("Wrong username or password. Try again.")
        count += 1

    return hostname

def removeFirstAndLastLine(output):
    line_list = output.split("\r\n")
    line_list = line_list[1:-1]
    output = ''
    for line in line_list:
        output = output + line + "\n"
    return output

def telnet_exec_command(obj, command, hostname, splitLines):
    """execute telnet command"""
    telnet_write(obj, command)
    output = telnet_read(obj, hostname)
    output = removeFirstAndLastLine(output)
    if splitLines:
        return output.splitlines(True)
    else:
        return output

################### file ####################
def selectDevice():
    global path_version, path_mac_port, path_trunk, path_run, path_cdp_detail, path_platform, path_portchannelSummary, path_portchannelDatabase, path_etherchannelSummary

    device = input("Select device [6513/3750/nexus]:")

    #device = "3750"
    path_version = 'files/version_{}.txt'.format(device)
    path_mac_port = 'files/mac_{}.txt'.format(device)
    path_trunk = 'files/trunk_{}.txt'.format(device)
    path_run = "files/run_{}.txt".format(device)
    path_cdp_detail = 'files/cdp_detail_{}.txt'.format(device)
    path_platform = 'files/hardwarePlatform.txt'
    path_portchannelSummary = "files/portchannel_summary_{}.txt".format(device)
    path_portchannelDatabase = "files/portchannel_database_{}.txt".format(device)
    path_etherchannelSummary = "files/etherchannel_summary_{}.txt".format(device)

def file_exec_command(command):
    if command == "show version":
        path = path_version
    elif command == "show mac address-table":
        path = path_mac_port
    elif command == "show interface trunk":
        path = path_trunk
    elif command == "show cdp neighbor detail":
        path = path_cdp_detail
    elif command == "show port-channel database":
        path = path_portchannelDatabase
    elif command == "show port-channel summary":
        path = path_portchannelSummary
    elif command == "show etherchannel summary":
        path = path_etherchannelSummary
    elif "show run int" in command:
        path = path_run

    with open(path, "r") as file_obj:
        if "channel" in command:
            output = file_obj.read().splitlines(True)
        else:
            output = file_obj.read()

    return output

################### common ##################
def is_valid_ip(ip):
    """checks if 'ip' is a valid ip"""
    ip_list = ip.split('.')
    if len(ip_list) < 4 or '' in ip_list:
        return False
    ip_list = [ int(x) for x in ip_list ]
    for i in range(4):
        if ip_list[i] < 0 or ip_list[i] > 255:
            return False
            break
        else:
            return True

def getIP():
    """get IP from the user"""
    while True:
        ip = input("IP address: ")
        if ip != '':
            if not is_valid_ip(ip):
                print("not a valid ip address")
            else:
                break
    return ip

def getHost():
    """get the ip to connect to"""
    host = getIP()

    return host

def getCredentials():
    """get the username and password"""
    username = input("Username: ")
    password = getpass.getpass()
    
    return username, password

def connect(o):
    """connect via ssh or telnet"""
    host = getHost()
    if o == 'ssh':
        """use paramiko to ssh into the switch"""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        while True:
            try:
                username, password = getCredentials()
                ssh.connect(host, username=username, password=password)
                print("Connected via SSH")
                return ssh
            except paramiko.ssh_exception.AuthenticationException:
                print("Wrong username or password. Try again.")
        return ssh
    elif o == 'tn':
        while True:
            """use telnetlib to telnet into the switch"""
            tn = telnetlib.Telnet()
            tn.open(host)
            username, password = getCredentials()
            hostname = login(tn, username, password)
            if hostname != '':
                return tn, hostname

def doCommand(obj, command, hostname=None, splitLines=False):
    """run command via ssh or telnet"""
    if isinstance(obj, paramiko.SSHClient):
        return ssh_exec_command(obj, command, splitLines)
    elif isinstance(obj, telnetlib.Telnet):
        return telnet_exec_command(obj, command, hostname, splitLines)
    elif obj == 'file':
        return file_exec_command(command)

def close(obj):
    """close the connection"""
    obj.close()
    if isinstance(obj, paramiko.SSHClient):
        print("SSH connection closed")
    elif isinstance(obj, telnetlib.Telnet):
        print("telnet connection closed")

################### switch commands ##################
def function_showVersion(obj, hostname=None):
    """
    executes 'show version'
    returns 'os_version'
    'os_version' is a string that contains either:
        "nexus" or "ios"
    """
    #EXEC: show version
    output = doCommand(obj, "show version", hostname)
    #place into list
    line_list = output.split('\n')  #one list
    version = []                                #list of lists
    for item in line_list:
        version.append(item.lower().split())
    #grab 'ios' or 'nexus'
    os_version = version[0][1]

    return os_version

def function_mac_port(obj, hostname=None):
    """
    executes 'show mac address-table'
    returns 'mac_port'
    'mac_port' is a list that contains:
        1. "MAC address" 2. "port"
        [[mac0, port0], [mac1, port1], ... ]
    """
    ### MAC_PORT ###
    #EXEC: show mac address-table
    output = doCommand(obj, "show mac address-table", hostname)
    #place into list
    line_list = output.split('\n')   #one list
    #remove the asterisk at the beginning of the line (if there is one)
    tmp = []
    for line in line_list:
        new_line = re.sub("^\*", "", line)
        tmp.append(new_line)
    line_list = tmp
    mac_port = []                                   #list of lists
    for item in line_list:
        mac_port.append(item.lower().split())
    #make note of where 'MAC' and 'Ports' columns are
    #get the header
    for item in mac_port:
        if 'type' in item:
            header = item
    #make each item in list lowercase
    tmp = []
    for item in header:
        tmp.append(item.lower())
    header = tmp
    #change 'ports/swid.ssid.lid' to 'ports' (NX-OS)
    tmp = []
    for item in header:
        if 'ports' in item:
            tmp.append('ports')
        else:
            tmp.append(item)
    header = tmp
    #remove 'address'
    tmp = []
    for item in header:
        if 'address' not in item:
            tmp.append(item)
    header = tmp
    #find index of 'mac' and 'ports'
    index_mac = header.index('mac')
    index_ports = header.index('ports')
    #remove header and static Type (remove all lines without dynamic in it)
    tmp = []
    for item in mac_port:
        if 'dynamic' in item:
            tmp.append(item)
    mac_port = tmp
    #remove all columns except MAC and Port columns
    tmp = []
    for item in mac_port:
        tmp.append([item[index_mac], item[index_ports]])    #MAC and Port
    mac_port = tmp

    return mac_port

def function_trunk(obj, hostname=None):
    """
    executes 'show interface trunk'
    returns 'trunk'
    'trunk' is a list that contains:
        1. "trunk port"
        [trunk_port0, trunk_port1, ... ]
    """
    ### TRUNK ###
    #EXEC: show interface trunk
    output = doCommand(obj, "show interface trunk", hostname)
    #place into list
    line_list = output.split('\n') #one list
    trunk = []                                  #list of lists
    for item in line_list:
        trunk.append(item.split())
    #remove all empty lines at beginning, keep first table and keep trailing empty line
    flag = False
    tmp = []
    for item in trunk:
        if item:                    #if not empty
            tmp.append(item)
            flag = True
        elif flag == True:          #if empty and flag is True
            tmp.append(item)
            break
    trunk = tmp
    #remove header for both NEXUS and other
    flag = False
    p = re.compile('tr')            #search line for 'trunking' or 'trnk-bndl'
    tmp = []
    for item in trunk:              #line
        for i in item:              #word
            m = p.match(i)
            if m != None:           #if 'tr' is found
                flag = True
                break
        if flag:                    #this line is not a header
            tmp.append(item)
    trunk = tmp
    #remove empty line at the end
    tmp = []
    for item in trunk:
        if item:
            tmp.append(item)
    trunk = tmp
    #remove all columns except Port column
    tmp = []
    for item in trunk:
        tmp.append(item[0].lower())
    trunk = tmp

    return trunk

def function_cdp_detail(obj, os_version, hostname=None):
    """
    executes 'show cdp neighbor detail'
    returns 'cdp_detail'
    'cdp_detail' is a list that contains:
        1. "interface" 2. "hardware platform"
        [[int0, hp0], [int1, hp1], ... ]
    """
    output = doCommand(obj, "show cdp neighbor detail", hostname)
    if os_version == 'ios':
        cdp_detail = output.split("-------------------------")
    elif os_version == 'nexus':
        cdp_detail = output.split("----------------------------------------")
    #outer list by entry. inner list by line
    tmp = []
    for entry in cdp_detail:
        tmp.append(entry.split('\n'))
    cdp_detail = tmp
    #remove empty list
    tmp = []
    for entry in cdp_detail:
        if len(entry) != 1:
            tmp.append(entry)
    cdp_detail = tmp
    #keep only Platform and Interface rows
    tmp = []
    index = 0
    for entry in cdp_detail:
        for i in range(len(entry)):
            if 'Platform:' in entry[i]:
                tmp.append([])
                tmp[index].append(entry[i])
            elif 'Interface:' in entry[i]:
                tmp[index].append(entry[i])
                index = index + 1
    cdp_detail = tmp
    #go through each inner list and only keep 
    #   1. platform name
    #   2. interface
    tmp = []
    index = 0
    for item in cdp_detail:
        tmp.append([])
        #1. interface 
        interface = item[1].split(',')
        interface = interface[0]
        #remove "Interface:"
        interface = interface.split(':')
        interface = interface[1].strip()
        tmp[index].append(interface)
        #2. platform
        platform = item[0].split(',')
        platform = platform[0]
        #remove "Platform:"
        platform = platform.split(':')
        platform = platform[1].strip()
        platform = platform.split()
        if len(platform) == 2:
            #remove "cisco "
            platform = platform[1]
        else:
            platform = platform[0]
        tmp[index].append(platform)
        index = index + 1
    cdp_detail = tmp

    return cdp_detail

def function_portchannel(obj, os_version, hostname=None):
    """
    executes 'show {port-channel | etherchannel} {database | summary}'
    returns 'portchannel'
    'portchannel' is a list that contains:
        1. "portchannel interface" 2. "physical interfaces"
        [[po0, phy0, phy1, ...], [po1, phy2, phy3, ...], ... ]
    """
    #trunk list contains the port channel interfaces
    #cdp list contains the physical interfaces
    if os_version == 'nexus':
        if command == 'database':
            output = doCommand(obj, "show port-channel database", hostname, True)
            tmp = [[]]
            index = 0
            for line in output:
                    if line == '\n':
                        tmp.append([])
                        index += 1
                    else:
                        tmp[index].append(line.strip()) #strip to remove spaces and newlines at beginning and ends of lines
            #remove the empty list at the end
            portchannel = tmp[0:-1]
            tmp = [[]]
            index = 0
            for item1 in portchannel:
                #port-channel## -> po##
                if item1:
                    tmp[index].append(item1[0].replace('port-channel', 'po'))
                    for item2 in item1:
                        #easy way to get all the physical interfaces that are up
                        if "active" in item2 and "up" in item2:
                            #only get "Ethernet#/#"
                            line = item2.split()
                            for word in line:
                                if "Ethernet" in word:
                                    #Ethernet#/# -> eth#/#
                                    tmp[index].append(word.replace('Ethernet', 'eth'))
                tmp.append([])
                index += 1
            #remove the empty list at the end
            tmp = tmp[0:-1]
            portchannel = tmp
        elif command == 'summary':
            #'show port-channel summary'
            #Group  Port-channel    Type    Protocol    Member Ports
            output = doCommand(obj, "show port-channel summary", hostname, True)
            #keep only what comes after the second set of '--' (hyphens)
            portchannel = []
            flag = 0
            index = -1 #needed in order to append line below to line above
            p = re.compile('^ +Eth.*') #used to search for 'Eth#/#(.)' that are on a different line
            for line in output:
                if "--" in line:
                    flag = flag + 1
                elif flag == 2:
                    index += 1
                    #if this should be appended to line above...
                    if p.match(line):
                        #1. line above: remove newline character at end
                        #2. line below: remove spaces at beginning
                        #3. concatenate
                        portchannel[index-1] = portchannel[index-1].strip('\n') + ' ' + line.strip(' ')
                    else:
                        portchannel.append(line)
            tmp2 = []
            for line in portchannel:
                #split by space
                row = line.split()
                tmp1 = []
                #append 'Port-channel'
                pch = re.sub("\(.*\)", "", row[1]) #removes parentheses and everything inside
                tmp1.append(pch.lower())
                #append all 'Ports'
                for i in range(len(row[4:])):
                    port = re.sub("\(.*\)", "", row[4+i]) #removes parentheses and everything inside
                    tmp1.append(port.lower())
                tmp2.append(tmp1)
            portchannel = tmp2
    else:
        #IOS 'show etherchannel summary'
        #Group  Port-channel    Protocol    Ports
        output = doCommand(obj, "show etherchannel summary", hostname, True)
        #keep only what comes after the '--' (hyphens)
        portchannel = []
        flag = False
        for line in output:
            if "--" in line:
                flag = True
            #print after hyphens and remove lines with only newlines and remove empty lines
            elif flag == True and line != '\n' and line != '':
                #split by space
                row = line.split()
                tmp = []
                #append 'Port-channel'
                pch = re.sub("\(.*\)", "", row[1]) #removes parentheses and everything inside
                tmp.append(pch.lower())
                #append all 'Ports'
                for i in range(len(row[3:])):
                    port = re.sub("\(.*\)", "", row[3+i]) #removes parentheses and everything inside
                    tmp.append(port.lower())
                portchannel.append(tmp)

    return portchannel

def update_trunk(obj, trunk, cdp_detail, portchannel, hostname=None):
    """
    updates the trunk list ('trunk') by removing trunk interfaces that have a hardware platform name not in 'path_platform'
    (Remove trunk interfaces that are connected to an ESXi server, WLC, etc...)
    returns 'trunk_updated'
    'trunk_updated' is a list that contains:
        1. "trunk port"
        [trunk_port0, trunk_port1, ... ]
    """
    #the platform list contains devices that should not be removed from the trunk file
    with open(path_platform, "r") as fo:
        platform = []
        for line in fo:
            platform.append(line.strip())
    #for each device in the cdp list
    r = []                              #interfaces to be removed from trunk list
    for item in cdp_detail:
        if item[1] not in platform:
            #place into a list
            r.append(item[0].lower())
    #abbreviate interface name. ex: change from 'gig' to 'gi'
    tmp = []
    for item in r:
        if 'fas' in item:
            tmp.append(item.replace('fastethernet', 'fa'))
        elif 'gig' in item:
            tmp.append(item.replace('gigabitethernet', 'gi'))
        elif 'ten' in item:
            tmp.append(item.replace('tengigabitethernet', 'te'))
        elif 'eth' in item:
            tmp.append(item.replace('ethernet', 'eth'))
    r = tmp
    #Interfaces to be removed from trunk list
    r1 = r

    #map physical interfaces to port channels and then append to r 
    tmp = []
    for item_r in r:
        #these are physical interfaces
        #let's find the port channel that it is bundled into, if applicable
        for item_pc in portchannel:
            if item_r in item_pc:
                tmp.append(item_pc[0])
    for item in tmp:
        r.append(item)
    #Interfaces to be removed from trunk list (including port channels)
    r2 = r

    #remove from trunk list
    tmp = []
    for item in trunk:
        if item not in r:
            tmp.append(item)
    trunk = tmp
    #trunk after removing cdp non-switches
    trunk_updated = trunk

    return trunk_updated

def update_mac_port(obj, mac_port_updated, trunk_updated, hostname=None):
    """
    updates the mac_port list ('mac_port') by removing trunk interfaces
    returns 'mac_port_updated'
    'mac_port_updated' is a list that contains:
        1. "MAC address" 2. "port"
        [[mac0, port0], [mac1, port1], ... ]
    """
    ### Modify MAC_PORT list ###
    #remove entries in mac_port list that are trunk
    tmp = []
    for item in mac_port_updated:
        if item[1] not in trunk_updated:
            tmp.append(item)
    mac_port_updated = tmp

    return mac_port_updated

def write_mac_config(mac_config):
    """write 'mac_config' list to file 'mac_config.txt'"""
    with open(path_mac_config, "w") as fo:
        for item1 in mac_config:
            fo.write(item1[0])  #mac address
            fo.write("\t")
            for item2 in item1[1]:  #write all the config lines
                fo.write(item2)
                fo.write("\t")
            fo.write("\n")

def create_mac_config(obj, mac_port_updated, hostname=None):
    """
    creates the list 'mac_config' and writes the file 'mac_config.txt'
    returns 'mac_config'
    'mac_config' is a list that contains:
        1. "MAC address" 2. [configurations]
        [[mac0, [conf00, conf01, ...]], [mac1, [conf10, conf11, conf12, ...]] ... ]
    'mac_config.txt' is a text file that contains:
        1. MAC address 2. configurations

        mac0 <TAB> conf00 <TAB> conf01 <NEWLINE>
        mac1 <TAB> conf10 <TAB> conf11 <TAB> conf12 <NEWLINE>
        etc ...
    """
    #get config for item in 'mac_port'
    mac_config = []
    for item in mac_port_updated:
        #write mac addresses
        mac_config.append([item[0]])
    #run 'show run int <interface>' for each interface in 'mac_port_updated'
    for i in range(len(mac_port_updated)):
        output = doCommand(obj, "show run int " + mac_port_updated[i][1], hostname)
        #create a list where each item is a line
        config_list = output.split('\n')
        #remove empty lines, and other unecessary lines
        tmp = []
        p = re.compile("^ .*") #lines that begin with a space
        for line in config_list:
            #these are the configs
            if p.match(line):
                tmp.append(line.strip())
        config_list = tmp
        #put in mac_config
        mac_config[i].append(config_list)
    write_mac_config(mac_config)

    return mac_config

def file_create_mac_config(os_version, mac_port_updated):
        """
        creates the list 'mac_config' and writes the file 'mac_config.txt'
        returns 'mac_config'
        'mac_config' is a list that contains:
            1. "MAC address" 2. [configurations]
            [[mac0, [conf00, conf01, ...]], [mac1, [conf10, conf11, conf12, ...]] ... ]
        'mac_config.txt' is a text file that contains:
            1. MAC address 2. configurations

            mac0 <TAB> conf00 <TAB> conf01 <NEWLINE>
            mac1 <TAB> conf10 <TAB> conf11 <TAB> conf12 <NEWLINE>
            etc ...
        """
        #get config for item in 'mac_port_updated'
        mac_config = []
        for item in mac_port_updated:
            #write mac addresses
            mac_config.append([item[0]])
        #open large running-config file
        with open(path_run, 'r') as fo:
            output = fo.read()
        #create a list where each item is split by '!'
        if os_version == "nexus":
            config_list = output.split('\n\n')
        elif os_version == "ios":
            config_list = output.split('!')
        #replace interface abbreviation with full name
        for i in range(len(mac_port_updated)):
            interface = mac_port_updated[i][1]
            if 'fa' in interface:
                interface = interface.replace('fa', 'FastEthernet')
            elif 'gi' in interface:
                interface = interface.replace('gi', 'GigabitEthernet')
            elif 'po' in interface:
                interface = interface.replace('po', 'Port-Channel')
            elif 'eth' in interface:
                interface = interface.replace('eth', 'Ethernet')
            for item in config_list:
                if interface in item:
                    #remove beginning and trailing newline characters and
                    # create a list where each word is an item
                    word_list = item.strip().split()
                    #needed so 1/0/4 does not match with 1/0/40
                    if interface in word_list:
                        #each line of the config is now an item in the list
                        line_list = item.strip().split('\n')
                        #remove 'interface' line
                        tmp = []
                        for item in line_list:
                            if 'interface' not in item:
                                tmp.append(item.strip())    #'strip' used to remove space at the front of line
                        line_list = tmp
                        mac_config[i].append(line_list)
                        #mac_config format is now [[MAC0, [CONFIG0]], [MAC1, [CONFIG1]], ...]
        write_mac_config(mac_config)

        return mac_config

def read_mac_config(obj, mac_port_updated, hostname=None):
    """
    reads the file 'mac_config.txt' and creates the list 'mac_config'
    returns 'mac_config'
    'mac_config' is a list that contains:
        1. "MAC address" 2. [configurations]
        [[mac0, [conf00, conf01, ...]], [mac1, [conf10, conf11, conf12, ...]] ... ]
    'mac_config.txt' is a text file that contains:
        1. MAC address 2. configurations

        mac0 <TAB> conf00 <TAB> conf01 <NEWLINE>
        mac1 <TAB> conf10 <TAB> conf11 <TAB> conf12 <NEWLINE>
        etc ...
    """
    #read from file 'mac_config.txt'
    line_list = []
    with open(path_mac_config, "r") as f:
        for line in f:
            line_list.append(line.strip())
    #re-create the mac_config list
    tmp = []
    for item in line_list:
        tmp.append(item.split('\t'))
    mac_config = tmp
    #put mac into 'tmp' and then remove it from 'mac_config'
    tmp = []
    for item in mac_config:
        tmp.append([item[0]])
        del item[0]
    #put the config into 'tmp'
    for i in range(len(mac_config)):
        tmp[i].append(mac_config[i])
    mac_config = tmp

    return mac_config

def usge(obj, hostname=None):
    """
    runs the functions that are common between 'retrieve' and 'configure' functions
    """
    os_version = function_showVersion(obj, hostname)
    print("os_version: {}".format(os_version))

    mac_port = function_mac_port(obj, hostname)
    print()
    print("mac_port")
    for item in mac_port:
        print(item)

    trunk = function_trunk(obj, hostname)
    print()
    print("trunk")
    for item in trunk:
        print(item)

    cdp_detail = function_cdp_detail(obj, os_version, hostname)
    print()
    print("cdp_detail")
    for item in cdp_detail:
        print(item)

    portchannel = function_portchannel(obj, os_version, hostname)
    print()
    print("portchannel")
    for item in portchannel:
        print(item)

    trunk_updated = update_trunk(obj, trunk, cdp_detail, portchannel, hostname)
    print()
    print("trunk updated")
    for item in trunk_updated:
        print(item)

    mac_port_updated = update_mac_port(obj, mac_port, trunk_updated, hostname)
    print()
    print("updated mac_port without trunk")
    for item in mac_port_updated:
        print(item)

    return mac_port_updated, os_version

def configuration(obj, mac_port_updated, mac_config):
    """
    configure the switch with the configurations in 'mac_config.txt'
    """
    print()
    print('**CONFIGURATION**')

    #EXEC: configure terminal
    ##ssh.exec_command("configure terminal")
    print("configure terminal")
    dup = [] #list of ports already configured
    count = 0 #number times duplicate port would have been configured
    for i in range(len(mac_config)):
        print(i)
        #mac address
        mac = mac_config[i][0]
        print("*mac: {}".format(mac))
        #use mac to lookup the port
        for item in mac_port_updated:
            if mac in item:
                port = item[1]
                print("*port: {}".format(port))
                #if this port is not in dup
                if port not in dup:
                    #add it to dup
                    dup.append(port)
                    #EXEC: int <port>
                    ##ssh.exec_command("interface " + port)
                    print("interface " + port)
                    #EXEC: <execute all commands in mac_config>
                    for config in mac_config[i][1]:
                        ##ssh.exec_command(config)
                        print(config)
                #skips configuring the same port
                else:
                    print("*port already configured, skipping...")
                    count += 1
        print()
    ##ssh.exec_command("end")
    print("end")

    print()
    dup.sort()
    print("ports that were configured")
    for item in dup:
        print(item)
    print()
    print("number of ports that were configured: {}".format(len(dup)))
    print("number of configurations saved: {}".format(count))

class ssh:
    def __init__(self):
        print()
        print("#"*85)
        print("#"*40 + " SSH " + "#"*40)
        print("#"*85)

    def retrieve(self):
        """creates 'mac_config.txt' which contains the mac address and configurations"""
        print("\n\n" + "#"*38 + " retrieve " + "#"*37)

        obj = connect('ssh')

        mac_port_updated, os_version = usge(obj)

        self.mac_config = create_mac_config(obj, mac_port_updated)
        print()
        print("mac_config")
        for item in self.mac_config:
            print(item)

        close(obj)

    def configure(self):
        print("\n\n" + "#"*38 + " configure " + "#"*37)

        obj = connect('ssh')

        mac_port_updated, os_version = usge(obj)

        self.mac_config = read_mac_config(obj, mac_port_updated)
        print()
        print("mac_config")
        for item in self.mac_config:
            print(item)

        configuration(obj, mac_port_updated, self.mac_config)

        close(obj)

class telnet:
    def __init__(self):
        print()
        print("#"*85)
        print("#"*38 + " telnet " + "#"*39)
        print("#"*85)

    def retrieve(self):
        """creates 'mac_config.txt' which contains the mac address and configurations"""
        print("\n\n" + "#"*38 + " retrieve " + "#"*37)

        obj, hostname = connect('tn')

        mac_port_updated, os_version = usge(obj, hostname)

        self.mac_config = create_mac_config(obj, mac_port_updated, hostname)
        print()
        print("mac_config")
        for item in self.mac_config:
            print(item)

        close(obj)

    def configure(self):
        print("\n\n" + "#"*38 + " configure " + "#"*37)

        obj, hostname = connect('tn')

        mac_port_updated, os_version = usge(obj, hostname)

        self.mac_config = read_mac_config(obj, mac_port_updated, hostname)
        print()
        print("mac_config")
        for item in self.mac_config:
            print(item)

        configuration(obj, mac_port_updated, self.mac_config)

        close(obj)

class file:
    def __init__(self):
        print()
        print("#"*85)
        print("#"*39 + " file " + "#"*40)
        print("#"*85)

    def retrieve(self):
        """creates 'mac_config.txt' which contains the mac address and configurations"""
        print("\n\n" + "#"*38 + " retrieve " + "#"*37)

        selectDevice()

        mac_port_updated, os_version = usge('file')

        self.mac_config = file_create_mac_config(os_version, mac_port_updated)
        print()
        print("mac_config")
        for item in self.mac_config:
            print(item)

    def configure(self):
        print("\n\n" + "#"*38 + " configure " + "#"*37)

        selectDevice()

        mac_port_updated, os_version = usge('file')

        self.mac_config = read_mac_config('file', mac_port_updated)
        print()
        print("mac_config")
        for item in self.mac_config:
            print(item)

        configuration('file', mac_port_updated, self.mac_config)
