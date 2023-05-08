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
            'ip helper-address': '-',
        }
        # hostname
        row['hostname'] = hostname

        # interface
        row['interface'] = intf_obj.text

        # description
        m_description = intf_obj.re_search_children(r'\s+description\s+(\S+)')
        if m_description:
            match = m_description[0].text.lstrip().rstrip().strip()
            line = re.split('description ', match)
            row['description'] = line[1]

        # shutdown
        m_shutdown = intf_obj.re_search_children(r'\s+shutdown$')
        if m_shutdown:
            match = m_shutdown[0].text.lstrip().rstrip().strip()
            row['shutdown'] = match
        
        # ip helper-address
        m_iphelper = intf_obj.re_search_children(r'\s+ip\s+helper-address\s+(\S+)$')
        if m_iphelper:
            l = []
            for i in m_iphelper:
                iphelper = re.findall('\s+ip\s+helper-address\s+(.*)$', i.text)[0]
                l.append(iphelper)
            row['ip helper-address'] = l

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