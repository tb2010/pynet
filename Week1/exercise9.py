#!/usr/bin/env python

""" Example 9 
    - read  cisco config 
    - print crypto sections using PFS group2
"""

from ciscoconfparse import CiscoConfParse

cfg_parser = CiscoConfParse('cisco_ipsec.txt')

crypto_lines = cfg_parser.find_objects_w_child(r'^crypto map CRYPTO', r'set pfs group2')

# set pfs group2 
for cline in crypto_lines:
    print cline.text
    
    for child in cline.children:
        print child.text

