#!/usr/bin/env python
'''
Class-based version....
Write a script that connects to the lab pynet-rtr1, logins, and executes the
'show ip int brief' command.
'''

import telnetlib
import time
import socket
import sys
import getpass

TELNET_PORT = 23
TELNET_TIMEOUT = 6

class TelnetConn(object):
    '''
    Telnet connection for cisco style network devices
    '''

    def __init__(self, ip_addr, username, password):
        self.ip_addr = ip_addr
        self.username = username
        self.password = password

        try:
            self.remote_conn = telnetlib.Telnet(self.ip_addr, TELNET_PORT, TELNET_TIMEOUT)
        except socket.timeout:
            sys.exit('Connection timed-out')

    def send_command(self, cmd):
        '''
        Send a command down the telnet channel
    
        Return the response
        '''
        cmd = cmd.rstrip()
        self.remote_conn.write(cmd + '\n')
        time.sleep(1)
        return self.remote_conn.read_very_eager()

    def login(self):
        '''
        Login to network device
        '''
        output = self.remote_conn.read_until("sername:", TELNET_TIMEOUT)
        self.remote_conn.write(self.username + '\n')
        output += self.remote_conn.read_until("ssword:", TELNET_TIMEOUT)
        self.remote_conn.write(self.password + '\n')
        return output

    def disable_paging(self, paging_cmd='terminal length 0'):
        '''
        Disable the paging of output (i.e. --More--)
        '''
        return self.send_command(paging_cmd)

    def close(self):
        '''
        Close telnet connection
        '''
        return self.remote_conn.close()


def main():
    '''
    Write a script that connects to the lab pynet-rtr1, logins, and executes the
    'show ip int brief' command.
    '''
    ip_addr = raw_input("IP address: ")
    ip_addr = ip_addr.strip()
    username = 'pyclass'
    password = getpass.getpass()

    telnet_conn = TelnetConn(ip_addr, username, password)
    telnet_conn.login()
    telnet_conn.disable_paging()
    output = telnet_conn.send_command('show ip int brief')

    print "\n\n"
    print output
    print "\n\n"

    telnet_conn.close()

if __name__ == "__main__":
    main()
