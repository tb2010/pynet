#!/usr/bin/env python

import time
import telnetlib

TELNET_PORT = 23
TELNET_TIMEOUT = 6

def main():
    ip_address = '184.105.247.70'
    username = 'pyclass'
    password = '88newclass'

    remote_conn = telnetlib.Telnet(ip_address, TELNET_PORT, TELNET_TIMEOUT)
    output = remote_conn.read_until('sername:', TELNET_TIMEOUT)
    print output
    remote_conn.write(username + '\n')
    output = remote_conn.read_until('assword:', TELNET_TIMEOUT)
    print output
    remote_conn.write(password + '\n')
    time.sleep(1)
    output = remote_conn.read_very_eager()
    print output
    remote_conn.write('show ip int brief' + '\n')
    time.sleep(1)
    output = remote_conn.read_very_eager()
    print output

    remote_conn.close()

if __name__ == "__main__":
    main()

