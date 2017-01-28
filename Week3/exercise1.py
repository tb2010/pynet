#!/usr/bin/env python
"""
Detect router changes using SNMPv3

If the running configuration has changed, send an email notification

use a Pickle file to store previous run results
"""

import os.path
import cPickle
from getpass import getpass
from datetime import datetime

from snmp_helper import snmp_get_oid_v3, snmp_extract
from email_helper import send_mail

# CONSTANTS

# 5 minutes in hundredths of seconds
RELOAD_INTERVAL = 5 * 60 * 100

# SNMP OIDs
OID_SYS_NAME = '1.3.6.1.2.1.1.5.0'
OID_SYS_UPTIME = '1.3.6.1.2.1.1.3.0'
OID_RC_LAST_CHANGED = '1.3.6.1.4.1.9.9.43.1.1.1.0'


def obtain_saved_info(file_name):
    """
    Read the Previously saved information

    file should contain a stored device objects...
    return will be a dictionary for those objects
    {
        'device_name': device_object,
        'device_name': device_object,
    }

    """

    # Check for existance of the file
    if not os.path.isfile(file_name):
        return {}

    saved_info = {}
    with open(file_name, 'r') as f:
        while True:
            try:
                cur_object = cPickle.load(f)
                saved_info[cur_object.device_name] = cur_object
            except EOFError:
                # No more data in file
                break

    return saved_info


def send_notification(net_device):
    """
    send notification based on network device passed in.
    """

    current_time = datetime.now()

    sender = 'wstanton@gmail.com'
    recipient = 'wstanton@gmail.com'
    subject = 'Device {0} was modified '.format(net_device.device_name)

    message = '''
The running configuration of {0} was modified.

This change was detected at: {1}

- The Notification System
'''.format(net_device.device_name, current_time)

    if send_mail(recipient, subject, message, sender):
        print "Notification sent to: {}".format(recipient)
        return True


class NetworkDevice(object):
    """Network Device Ojbject"""

    def __init__(self, device_name, uptime, last_changed, config_changed=False):
        self.device_name = device_name
        self.uptime = uptime
        self.last_changed = last_changed
        self.config_changed = config_changed


def main():
    save_file = 'saved_info.pkl'

    rtr1_ip_addr = '184.105.247.70'
    rtr2_ip_addr = '184.105.247.71'
    auth_enc_key = getpass(prompt="Authen & Encrypt Key: ")

    cur_user = 'pysnmp'
    auth_key = auth_enc_key
    enc_key = auth_enc_key

    snmp_user = (cur_user, auth_key, enc_key)
    pynet_rtr1 = (rtr1_ip_addr, 161)
    pynet_rtr2 = (rtr2_ip_addr, 161)
    all_devices = (pynet_rtr1, pynet_rtr2)

    saved_info = obtain_saved_info(save_file)

    cur_info = {}

    for cur_device in all_devices:
        snmp_results = []
        if __name__ == '__main__':
            for cur_oid in (OID_SYS_NAME, OID_SYS_UPTIME, OID_RC_LAST_CHANGED):
                try:
                    value = snmp_extract(snmp_get_oid_v3(cur_device, snmp_user, oid=cur_oid))
                    snmp_results.append(int(value))
                except ValueError:
                    # value isn't an integer so add it as a string....
                    snmp_results.append(value)

            # Now extract the temporary array to individual variables (assumes order)
            device_name, uptime, last_changed = snmp_results

            if device_name in saved_info:
                saved_device = saved_info[device_name]

                if uptime < saved_device.uptime or last_changed < saved_device.last_changed:
                    if last_changed <= RELOAD_INTERVAL:
                        # device reloaded, but not changed
                        cur_info[device_name] = NetworkDevice(device_name, uptime, last_changed, False)
                    else:
                        # device reloaded and changed
                        cur_info[device_name] = NetworkDevice(device_name, uptime, last_changed, True)
                elif last_changed == saved_device.last_changed:
                    # no change
                    cur_info[device_name] = NetworkDevice(device_name, uptime, last_changed, False)
                elif last_changed > saved_device.last_changed:
                    # running configuration was changed
                    cur_info[device_name] = NetworkDevice(device_name, uptime, last_changed, True)
                    send_notification(cur_info[device_name])
                else:
                    raise ValueError()
            else:
                # new device.... just add it to the list
                cur_info[device_name] = NetworkDevice(device_name, uptime, last_changed, False)

    # Write the information to the save file
    with open(save_file, 'w') as f:
        for device_object in cur_info.values():
            cPickle.dump(device_object, f)


if __name__ == "__main__":
    main()

