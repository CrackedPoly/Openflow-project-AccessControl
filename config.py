# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     config.py
   Description :
   Author :       unstoppable
   date：          4/1/2022
-------------------------------------------------
   Change Activity:
                   4/1/2022:
-------------------------------------------------
"""
ODL_ip = "172.16.86.1"
ODL_rest_addr = "http://172.16.86.1:8181"

user_list = [
    {
        "username": "Alice",
        "password": "Alice",
        "groups": ["print_office"],
    },
    {
        "username": "Bob",
        "password": "Bob",
        "groups": ["print_office"],
    },
    {
        "username": "Cindy",
        "password": "Cindy",
        "groups": ["web_office"],
    },
    {
        "username": "David",
        "password": "David",
        "groups": ["web_office"],
    },
    {
        "username": "root",
        "password": "root",
        "groups": ["root"],
    },
]

group_list = ["print_office", "web_office", "root"]

# 0 for not seeing, discarding any packets
# 1 for ping, only allowing ICMP and ARP
# 2 for access, allowing all packets
device_list = [
    {
        "devicename": "AC_server",
        "owner": "root",
        "group": "root",
        "permission": "222",
        "mac": "12:34:56:78:00:01",
        "ip": "10.0.0.1/8",
    },
    {
        "devicename": "printer",
        "owner": "Alice",
        "group": "print_office",
        "permission": "220",
        "mac": "12:34:56:78:00:02",
        "ip": "10.0.0.2/8",
    },
    {
        "devicename": "web_server",
        "owner": "Cindy",
        "group": "web_office",
        "permission": "221",
        "mac": "12:34:56:78:00:03",
        "ip": "10.0.0.3/8",
    }
]
