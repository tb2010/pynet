#!/usr/bin/env python
"""
Exercise 2

Using SNMPv3 create two SVG image files.

The first image file should graph the input and output octets on interface FA4 on pynet-rtr1 every five minutes
for an hour.  Use the pygal library to create the SVG graph file. Note, you should be doing a subtraction here
 (i.e. the input/output octets transmitted during this five minute interval).

The second SVG graph file should be the same as the first except graph the unicast packets received and transmitted.

"""

import time
from getpass import getpass

from snmp_helper import snmp_get_oid_v3, snmp_extract
import line_graph


def get_interface_stats(snmp_device, snmp_user, stat_type, if_index):
    """
    statue-type can be 'in_octets, out_octets, in_ucast_pkts or out_ucast_pkts'

    returns the counter value as an integer
    """

    oid_dict = {
        'in_octets': '1.3.6.1.2.1.2.2.1.10',
        'out_octets': '1.3.6.1.2.1.2.2.1.16',
        'in_ucast_pkts': '1.3.6.1.2.1.2.2.1.11',
        'out_ucast_pkts': '1.3.6.1.2.1.2.2.1.17',
    }

    if stat_type not in oid_dict.keys():
        raise ValueError("Invalid stat_type selected: {}" % stat_type)

    if_index = int(if_index)

    oid = oid_dict[stat_type]
    oid = oid + '.' + str(if_index)

    snmp_data = snmp_get_oid_v3(snmp_device, snmp_user, oid)
    return int(snmp_extract(snmp_data))


def main():
    # SNMPv3 Connection Parameters
    rtr1_ip_addr = raw_input("Enter device IP: ")
    auth_enc_key = getpass(prompt="Auth & Encryption Key: ")

    v3_user = 'pysnmp'
    auth_key = auth_enc_key
    encr_key = auth_enc_key

    snmp_user = (v3_user, auth_key, encr_key)
    snmp_device = (rtr1_ip_addr, 161)

    # Fa4 Interface Index is number 5 in the lab routers
    if_index = 5
    graph_stats = {
        "in_octets": [],
        "out_octets": [],
        "in_ucast_pkts": [],
        "out_ucast_pkts": [],
    }
    base_count_dict = {}

    # for 0 - 65 stepping by 5
    for time_track in range(0, 65, 5):
        print "%20s %-60s" % ("time", time_track)

        for entry in ("in_octets", "out_octets", "in_ucast_pkts", "out_ucast_pkts"):
            snmp_count = get_interface_stats(snmp_device, snmp_user, entry, if_index)
            base_count = base_count_dict.get(entry)
            if base_count:
                graph_stats[entry].append(snmp_count - base_count)
                print "%20s %-60s" % (entry, graph_stats[entry][-1])
            base_count_dict[entry] = snmp_count
        time.sleep(10)

    x_labels = []
    for x_label in range(5, 65, 5):
        x_labels.append(str(x_label))

    if line_graph.twoline("rtr1-octets.svg", "rtr1 Fa4 Input/Output Bytes",
                          graph_stats["in_octets"], "In Octets",
                          graph_stats["out_octets"], "Out Octets", x_labels):
        print "In/Out Octet graph created"

    if line_graph.twoline('rtr1-packets.svg', 'rtr1 Fa4 Input/Output Packets',
                          graph_stats['in_ucast_pkts'], 'In Packets',
                          graph_stats['out_ucast_pkts'], 'Out Packets', x_labels):
        print "In/Out Packet graph created"


if __name__ == "__main__":
    main()

