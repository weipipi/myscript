#!/usr/bin/python
import fileinput
import re
import sys
import datetime
from glob import glob

if __name__ == '__main__':
    myconf = sys.argv[1]

    blocks = {}
    for line in fileinput.input(myconf):
        mathblockbegin = re.search('^!.*<([A-Z].*?)>', line)
        mathblockend = re.search('^!.*<\/', line)

        if mathblockbegin :
            blockname = mathblockbegin.group(1)
            blocks[blockname] = []
        elif mathblockend :
            blockname = 'BLACK'
        else :
            blocks[blockname].append(line.rstrip() )

    #VRF
    vrfsbyname = {}
    vrfsbyid = {}
    for bline in blocks['VRF'] :
        mathvrf = re.search('^ip vrf (\S*) vpnid (\d*)', bline)
        mathseend = re.search('^!', bline)

        if mathvrf :
            vrfname = mathvrf.group(1)
            vrfid = mathvrf.group(2)
            
            vrfsbyname[vrfname] = [bline]
            vrfsbyid[vrfid] = [bline]
        elif mathseend :
            vrfname = vrfid = ''
        else :
            vrfsbyname[vrfname].append(bline)
            vrfsbyid[vrfid].append(bline)

    #INTERFACE
    interfaces = {}
    for bline in blocks['INTERFACE'] :
        mathif = re.search('^interface (\S*)', bline)
        mathseend = re.search('^!', bline)

        if mathif :
            ifname = mathif.group(1)
            interfaces[ifname] = [bline]
        elif mathseend :
            ifname = ''
        else :
            interfaces[ifname].append(bline)

    #VLAN
    vlans = {}
    for bline in blocks['VLAN'] :
        if re.search('vlan-configuration', bline) : 
            continue
        
        mathvlan = re.search('^\s*interface (\S*)', bline)
        mathseend = re.search('\$', bline)

        if mathvlan :
            vlanifname = mathvlan.group(1)
            vlans[vlanifname] = ['vlan-configuration',bline]
        elif mathseend :
            vlanifname = ''
        else :
            vlans[vlanifname].append(bline)
            
    for sline in vlans['gei-0/9/1/5.2100'] : 
        print sline
