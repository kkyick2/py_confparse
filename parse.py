import os
import re
import pandas as pd
from ciscoconfparse import CiscoConfParse



def parseConfig(inf):
    '''
        @inf : input config txt file
        @d: return a list of dict
            [{'hostname': 'ES-B15W-1', 'interface': 'interface Loopback0', 'shutdown': '-', 'description': '-'}, 
             {'hostname': 'ES-B15W-1', 'interface': 'interface Loopback0', 'shutdown': '-', 'description': '-'}, ...]
    '''
    d = []
    parse = CiscoConfParse(inf)
    # hostname 
    hostname_obj = parse.find_objects(r'^hostname')[0]
    hostname = hostname_obj.re_match_typed(r'^hostname\s+(\S+)', default='')

    # intf_cmds: list of intf objects eg, [<IOSCfgLine # 258 'interface GigabitEthernet1/1'>, <> ...]
    all_intfs = parse.find_objects(r"^interface ")
    for intf_obj in all_intfs: 
        print('----------')
        print(intf_obj.text)
        print(intf_obj.children)
        row = {
            'hostname' : '-',
            'interface' : '-',
            'shutdown' : '-',
            'description' : '-',
            'port_mode' : '-',
            'channel-group': '-',
            'ip address': '-',
            'vrf': '-',
            'ip helper-address' : '-',
            'ip access-group': '-',
        }
        # hostname
        row['hostname'] = hostname

        # interface
        row['interface'] = intf_obj.text

        for intf_child in intf_obj.children:
            print('-----')
            line = intf_child.text.lstrip().rstrip().strip()
            '''
                <line>
                description Blg15W-G/F-IP-Phone
            '''

            # shutdown
            if line.startswith('shutdown'):
                row['shutdown'] = line

            # description
            if line.startswith('description'):
                line2 = re.split('description ', line)
                row['description'] = line2[1]

            # mode
            if line.startswith('switchport mode'):
                line2 = re.split('switchport mode ',line)
                row['port_mode'] = line2[1]

            # channel-group
            if line.startswith('channel-group'):
                row['channel-group'] = line

            # ip address
            if line.startswith('ip address'):
                line2 = re.split('ip address ', line)
                row['ip address'] = line2[1]

            # vrf
            if line.startswith('vrf forwarding') | line.startswith('ip vrf forwarding') | line.startswith('vrf member') :
                line2 = re.split('vrf forwarding ', line)
                row['vrf'] = line2[1]

            # ip helper-address
            if line.startswith('ip helper-address'):
                #print(line)
                match = re.findall(r'ip\s+helper-address\s+(\S+)$', line)
                #print(match)

            # ip access-group
            if line.startswith('ip access-group'):
                line2 = re.split('ip access-group ', line)
                row['ip access-group'] = line2[1]

        d.append(row)
    
    return d


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


def main():
    dir = os.path.dirname(__file__)
    indir = 'config'
    outdir = 'output'

    infile = 'ES-B15W-2.cfg'
    outfile = infile + '_out.csv'
    inf = os.path.join(dir, indir, infile)
    outf = os.path.join(dir, outdir, outfile)

    dict = parseConfig(inf)
    df1 = pd.DataFrame(dict)
    print('--------------')
    print(df1)
    output_dataframe(df1, [outf, 'sheet1'])


if __name__ == "__main__":
    main()