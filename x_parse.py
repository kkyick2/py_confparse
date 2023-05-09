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
    # all_intfs: list of intf objects eg, 
    # [ <IOSCfgLine # 258 'interface GigabitEthernet1/1'>, 
    #   <IOSCfgLine # 261 'interface GigabitEthernet1/2'>, ...]
    all_intfs = parse.find_objects(r"^interface ")
    for intf_obj in all_intfs:
        row = {
            'hostname' : '-',
            'interface' : '-',
            'shutdown' : '-',
            'description' : '-',
            'mode' : '-',
            'channel-group' : '-',
            'ipaddr' : '-',
            'helper-address': '-',
            'access-group': '-',
            'standby group': '-',
            'standby ip': '-',
            'standby setting': '-',
        }
        # hostname
        row['hostname'] = hostname

        # interface
        row['interface'] = intf_obj.text

        # shutdown
        m_shut = intf_obj.re_search_children(r'\s+shutdown$')
        if m_shut:
            match = m_shut[0].text.lstrip().rstrip().strip()
            row['shutdown'] = match
        
        # description
        m_desc = intf_obj.re_search_children(r'\s+description\s+(\S+)')
        if m_desc:
            match = m_desc[0].text.lstrip().rstrip().strip()
            line = re.split('description ', match)
            row['description'] = line[1]
        #################################################
        # switchport mode
        m_mode = intf_obj.re_search_children(r'\s+switchport\s+mode\s+(\S+)')
        if m_mode:
            match = m_mode[0].text.lstrip().rstrip().strip()
            line = re.split('switchport mode ', match)
            row['mode'] = line[1]
        
        # channel-group
        m_po = intf_obj.re_search_children(r'\s+channel-group\s+\d+\s+mode\s+(\S+)$')
        if m_po:
            match = m_po[0].text.lstrip().rstrip().strip()
            line = re.split('channel-group ', match)
            row['channel-group'] = line[1]

        #################################################
        # ip address
        m_ipaddr = intf_obj.re_search_children(r'\s+ip\s+address\s+(\S+)')
        if m_ipaddr:
            match = m_ipaddr[0].text.lstrip().rstrip().strip()
            line = re.split('ip address ', match)
            row['ipaddr'] = line[1]

        # ip helper-address
        m_iphelper = intf_obj.re_search_children(r'\s+ip\s+helper-address\s+(\S+)$')
        if m_iphelper:
            l = []
            for i in m_iphelper:
                iphelper = re.findall(r'\s+ip\s+helper-address\s+(.*)$', i.text)[0]
                l.append(iphelper)
            row['helper-address'] = l

        # ip access-group
        m_ipaccessgp = intf_obj.re_search_children(r'\s+ip\s+access-group\s+(.+)$')
        if m_ipaccessgp:
            match = m_ipaccessgp[0].text.lstrip().rstrip().strip()
            line = re.split('ip access-group ', match)
            row['access-group'] = line[1]

        # standby 100 ip 1.1.1.1
        m_standby = intf_obj.re_search_children(r'\s+standby\s+\d+\s(.+)$')
        if m_standby:
            l = []
            for i in m_standby:
                abc = re.findall(r'\s+standby\s+(\d+)\s+ip\s+(.+)', i.text)
                print(abc)
            #'standby group': '-',
            #'standby setting': '-',

        print(row)
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

    infile = 'ES-B16W-1.cfg'
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