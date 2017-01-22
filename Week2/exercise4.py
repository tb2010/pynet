#!/usr/bin/env python
'''
Create a script that connects to the lab routers and prints
out both the MIB2 sysName and sysDescr info.
'''

import getpass
import snmp_helper

MIB2_SYS_DESCR = '1.3.6.1.2.1.1.1.0'
MIB2_SYS_NAME = '1.3.6.1.2.1.1.5.0'

def main():
    '''
    Get the IP addresses of both routers and the community string ....
    '''
    ip_addr1 = raw_input('pynet-rtr1 IP Address: ')
    ip_addr2 = raw_input('pynet-rtr2 IP Address: ')
    community_string = getpass.getpass(prompt='Community String: ')

    pynet_rtr1 = (ip_addr1, community_string, 161)
    pynet_rtr2 = (ip_addr2, community_string, 161)

    for cur_device in (pynet_rtr1, pynet_rtr2):
        print "*********"
        for cur_oid in (MIB2_SYS_NAME, MIB2_SYS_DESCR):
            snmp_data = snmp_helper.snmp_get_oid(cur_device, oid=cur_oid)
            output = snmp_helper.snmp_extract(snmp_data)

            print output
        print "*********"
    print

if __name__ == '__main__':
    main()
