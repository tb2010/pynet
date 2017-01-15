#!/usr/bin/env python

""" Example 8 
    - read  cisco config 
    - print crypto sections will all children
"""

from ciscoconfparse import CiscoConfParse

cfg_parser = CiscoConfParse('cisco_ipsec.txt')

crypto_lines = cfg_parser.find_objects(r'^crypto map CRYPTO')

for cline in crypto_lines:
    print cline.text
    
    for child in cline.children:
        print child.text

