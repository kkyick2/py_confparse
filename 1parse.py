import os
import re
import pandas as pd
from ciscoconfparse import CiscoConfParse



def parseConfig(inf):
    '''
        @inf : input config txt file
        @rtl: return a list of dict
            [{'hostname': 'ES-B15W-1', 'interface': 'interface Loopback0', 'shutdown': '-', 'description': '-'}, 
             {'hostname': 'ES-B15W-1', 'interface': 'interface Loopback0', 'shutdown': '-', 'description': '-'}, ...]
    '''
    rtl = []
    parse = CiscoConfParse(inf)
    #################################################
    # hostname 
    hostname_obj = parse.find_objects(r'^hostname')[0]
    hostname = hostname_obj.re_match_typed(r'^hostname\s+(\S+)', default='')
    print("--hostname: {}".format(hostname))
    #################################################
    # all_intfs: list of intf objects example:
    # [ <IOSCfgLine # 258 'interface GigabitEthernet1/1'>, 
    #   <IOSCfgLine # 261 'interface GigabitEthernet1/2'>, ...]    
    all_intfs = parse.find_objects(r"^interface ")
    for intf_obj in all_intfs: 

        l_iphelper = []
        l_standby = []
        l_ippim = []
        l_ipigmp = []
        l_noipxxx = []
        l_oth_cmd = []
        row = {
            'hostname' : '-',
            'interface' : '-',
            'shutdown' : '-',
            'description' : '-',
            'port_mode' : '-',
            'trunk vlan': '-',
            'access vlan': '-',
            'channel-group': '-',
            'ipaddr': '-',
            'vrf': '-',
            'helper-address' : '-',
            'access-group': '-',
            'standby': '-',
            'ippim': '-',
            'ipigmp': '-',
            'no ip xxx': '-',
            'other': '-',
        }
        # hostname
        row['hostname'] = hostname

        # interface
        intf2 = re.split('interface ', intf_obj.text)[1]
        row['interface'] = intf2
        # print("--interface: {}".format(intf2))
        #################################################
        # print("----intf_child: {}".format(intf_obj.children))
        for intf_child in intf_obj.children:
            line = intf_child.text.lstrip().rstrip().strip()
            '''
                description Blg15W-G/F-IP-Phone
            '''
            # shutdown
            if line.startswith('shutdown'):
                row['shutdown'] = line

            # description
            elif line.startswith('description'):
                line2 = re.split('description ', line)
                row['description'] = line2[1]

            #################################################
            # switchport mode
            elif line.startswith('switchport mode'):
                line2 = re.split('switchport mode ',line)
                row['port_mode'] = line2[1]

            # channel-group
            elif line.startswith('channel-group'):
                row['channel-group'] = line

            # switchport access vlan
            elif line.startswith('switchport access vlan'):
                line2 = re.split('switchport access vlan ',line)
                row['access vlan'] = line2[1]

            # switchport trunk allowed vlan
            elif line.startswith('switchport trunk allowed vlan'):
                line2 = re.split('switchport trunk allowed vlan ',line)
                row['trunk vlan'] = line2[1]

            #################################################
            # ip address
            elif line.startswith('ip address'):
                line2 = re.split('ip address ', line)
                row['ipaddr'] = line2[1]

            # vrf
            elif line.startswith('vrf forwarding') | line.startswith('ip vrf forwarding') | line.startswith('vrf member') :
                line2 = re.split('vrf forwarding ', line)
                row['vrf'] = line2[1]

            # ip helper-address
            # multiple match, put in list
            elif line.startswith('ip helper-address'):
                line2 = re.findall(r'ip\s+helper-address\s+(\S+)$', line)
                l_iphelper.append(line2[0])
                
            # ip access-group
            elif line.startswith('ip access-group'):
                line2 = re.split('ip access-group ', line)
                row['access-group'] = line2[1]

            # standby 1 ip 10.95.138.1, standby 1 prioity 50, ...etc
            # multiple match, put in list
            elif line.startswith('standby'):
                line2 = re.findall(r'standby\s+(.+)', line)
                l_standby.append(line2[0])

            # ip pim
            # multiple match, put in list
            elif line.startswith('ip pim'):
                line2 = re.findall(r'ip pim\s+(.+)', line)
                l_ippim.append(line2[0])

            # ip igmp
            # multiple match, put in list
            elif line.startswith('ip igmp'):
                line2 = re.findall(r'ip igmp\s+(.+)', line)
                l_ipigmp.append(line2[0])

            # no ip redirects, no ip unreachables, no ip proxy-arp
            # multiple match, put in list
            elif line.startswith('no ip redirects') | line.startswith('no ip unreachables') | line.startswith('no ip proxy-arp'):
                line2 = re.findall(r'no\s+ip\s+(.+)', line)
                l_noipxxx.append(line2[0])
            #################################################
            # other child in intf
            else:
                l_oth_cmd.append(line)

        # Append row to list d
        if l_iphelper:
            row['helper-address'] = l_iphelper
        if l_standby:
            row['standby'] = l_standby
        if l_ippim:
            row['ippim'] = l_ippim
        if l_ipigmp:
            row['ipigmp'] = l_ipigmp
        if l_noipxxx:
            row['no ip xxx'] = l_noipxxx
        if l_oth_cmd:
            row['other'] = l_oth_cmd
        rtl.append(row)
    
    return rtl


def output_dataframe(df, outf):
    '''
        @df : pandas dataframe
        @outf: a list include [filename,sheetname]
    '''
    print("Prepare export to file: ")
    # option1: Excel
    # df.to_excel(outf[0], sheet_name=outf[1], index=False)
    # option2: CSV
    df.to_csv(outf[0], index=False)

    print("Export dataframe to file: {}".format(outf[0]))
    return


def start_script(input_cfg):
    dir = os.path.dirname(__file__)
    indir = 'config'
    outdir = 'output'

    infile = input_cfg
    outfile = infile + '_out.csv'
    inf = os.path.join(dir, indir, infile)
    outf = os.path.join(dir, outdir, outfile)
    #################################################
    print("="*50)
    print("Start Parsing input file: {}".format(inf))
    dict = parseConfig(inf)
    #################################################
    df1 = pd.DataFrame(dict)
    print("-"*25)
    print(df1)
    output_dataframe(df1, [outf, 'sheet1'])
    print("="*50)
    return df1


def main():
    input_cfg_list = [
        'ES-B15W-1.cfg',
        'ES-B15W-2.cfg',
        'ES-B16W-1.cfg',
        'ES-B16W-2.cfg',
    ]
    for input_cfg in input_cfg_list:
        df = start_script(input_cfg)




    merage_dataframe()

if __name__ == "__main__":
    main()