__author__ = 'ykk'

from ciscoconfparse import CiscoConfParse
import os
import csv
import sys
import re
from os import listdir
from os.path import isfile, join

filedir = os.path.dirname(__file__)
inputdir = 'config'
outputdir = 'output'

inputfilelist = [f for f in listdir(inputdir) if isfile(join(inputdir, f))]

# backwards compatibility for python3 and python2 csv writer
def open_csv(filename, mode):
    """
    Open a csv file in proper mode depending on Python verion.
    with open (outfilename, 'wb') as outF: 					# this code is for python2
    with open (outfilename, 'w', newline='') as outF:	 	# this code is for python3
    """
    return open(filename, mode=mode + 'b') if sys.version_info[0] == 2 else open(filename, mode=mode, newline='')


def writeRow(outF, row):
    writer = csv.writer(outF)
    writer.writerow(row)


def parseCisco2(inputfilename, inputfilenamefull):
    # option1: each device output file
    # outputfilename = inputfilename + '_out.csv'
    # option2: append to one output files\
    outputfilename = inputfilename + '_out.csv'

    outputfilenamefull = os.path.join(filedir, outputdir + '/' + outputfilename)
    parse = CiscoConfParse(inputfilenamefull)
    print(parse)

    order_keys = []
    HOSTNAME = 'HOSTNAME'
    INT_NAME = 'INT_NAME'
    SHUTDOWN = 'SHUTDOWN'
    DESCRIPTION = 'DESCRIPTION'
    INT_MODE = 'INT_MODE'
    TRUNK = 'TRUNK'
    ACCESS = 'ACCESS'
    PO = 'PO'
    IPADDR = 'IPADDR'
    VRF = 'VRF'
    OSPF = 'OSPF'
    HSRP = 'HSRP'
    IP_ACCESS_GP = 'IP_ACCESS_GP'

    order_keys.append(HOSTNAME)
    order_keys.append(INT_NAME)
    order_keys.append(SHUTDOWN)
    order_keys.append(DESCRIPTION)
    order_keys.append(INT_MODE)
    order_keys.append(TRUNK)
    order_keys.append(ACCESS)
    order_keys.append(PO)
    order_keys.append(IPADDR)
    order_keys.append(VRF)
    order_keys.append(OSPF)
    order_keys.append(HSRP)
    order_keys.append(IP_ACCESS_GP)

    # hostname
    global_obj = parse.find_objects(r'^hostname')[0]
    hostname = global_obj.re_match_typed(r'^hostname\s+(\S+)', default='')

    # loop each interface
    rtr_interfaces = parse.find_objects(r"^interface ")
    with open_csv(outputfilenamefull, 'a') as outF:
        writer = csv.writer(outF)
        
        writeRow(outF, order_keys)
        
        for interface in rtr_interfaces:

            #print(interface.text)
            host = hostname
            shutdown = 'na'
            description = 'na'
            switchport_mode = 'na'
            access = 'na'
            trunk = 'na'
            po = 'na'
            stp = 'na'
            ipaddr = 'na'
            vrf = 'na'
            ip_ospf = 'na'
            standby = 'na'
            ipaccessgroup = 'na'

            for children in interface.children:
                line = children.text
                line = line.lstrip().rstrip().strip()
                #print(line)

                if line.startswith('shutdown'):
                    shutdown = line
                    #print(shutdown)

                if line.startswith('description'):
                    line2 = re.split('description ',line)
                    #print(line2[1])
                    description = line2[1]
                    #print(description)

                if line.startswith('switchport mode'):
                    line2 = re.split('switchport mode ',line)
                    switchport_mode = line2[1]
                    #print(switchport_mode)

                if line.startswith('switchport access vlan'):
                    access = line
                    #print(access)

                if line.startswith('switchport trunk'):
                    access = line
                    #print(trunk)

                if line.startswith('channel-group'):
                    po = line
                    #print(po)

                if line.startswith('ip address'):
                    ipaddr = line
                    #print(ipaddr)
                    
                if line.startswith('ip ospf'):
                    ip_ospf = line

                if line.startswith('standby'):
                    re1= re.compile('standby (.*) ip (.*)')
                    if(re1.search(line)):
                        (a,b) = re.findall('standby (.*) ip (.*)', line)[0]
                        standby = b

                if line.startswith('ip access-group'):
                    ipaccessgroup = line
                    
                if line.startswith('vrf forwarding') | line.startswith('ip vrf forwarding') | line.startswith('vrf member') :
                    vrf = line
                    #print(vrf)

            outputRow = []
            print((host, interface.text, shutdown, description, switchport_mode, access, trunk, po, ipaddr, vrf, ip_ospf, standby, ipaccessgroup))
            outputRow.extend((host, interface.text, shutdown, description, switchport_mode, access, trunk, po, ipaddr, vrf, ip_ospf, standby, ipaccessgroup))
            writeRow(outF, outputRow)


for filename in inputfilelist:
    inputfilenamefull = os.path.join(filedir, inputdir + '/' + filename)
    print(inputfilenamefull)
    parseCisco2(filename, inputfilenamefull)
