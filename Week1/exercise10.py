#!/usr/bin/env python

""" Example 10 
    - read  cisco config 
    - print crypto sections using AES (use transform name)
"""

from ciscoconfparse import CiscoConfParse

cfg_parser = CiscoConfParse('cisco_ipsec.txt')

crypto_lines = cfg_parser.find_objects_wo_child(r'^crypto map CRYPTO', r'transform-set AES')

for cline in crypto_lines:
    print cline.text
    
    for child in cline.children:
        print child.text

