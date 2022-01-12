# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     tools.py
   Description :
   Author :       unstoppable
   date：          5/1/2022
-------------------------------------------------
   Change Activity:
                   5/1/2022:
-------------------------------------------------
"""
import json
import requests
import sys

from .template import *
sys.path.append("..")
from AC.config import ODL_rest_addr


# enable flow from host1 to host2, unidirectional
def enable_flow(protocol, vSwitch, hostname1, hostmac1, hostname2, hostmac2, **kwargs):
    url = f"{ODL_rest_addr}/restconf/config/opendaylight-inventory:nodes/node/openflow:{vSwitch[1:]}/table/0" \
          f"/flow/{vSwitch}-{protocol}-all-{hostname1}-{hostname2}"
    json_obj = json.loads(flow_template % (vSwitch, protocol, "all", hostname1, hostname2))

    if protocol == "arp":
        arp_op = kwargs["op"]
        if arp_op == 1:
            arp_type = "request"
            output_action = "FLOOD"
            json_obj = json.loads(flow_template % (vSwitch, protocol, arp_type, hostname1, hostname2))
            json_obj = add_match(json_obj, arp_request_match_template)
        elif arp_op == 2:
            arp_type = "reply"
            arp_target_mac = hostmac2
            output_action = "NORMAL"
            json_obj = json.loads(flow_template % (vSwitch, protocol, arp_type, hostname1, hostname2))
            json_obj = add_match(json_obj, arp_match_template % (hostmac1, arp_target_mac, arp_op))
        else:
            raise Exception("unsupported arp operation code")
        url = f"{ODL_rest_addr}/restconf/config/opendaylight-inventory:nodes/node/openflow:{vSwitch[1:]}/table/0" \
              f"/flow/{vSwitch}-{protocol}-{arp_type}-{hostname1}-{hostname2}"
        json_obj = add_action(json_obj, action_template % output_action)
    elif protocol == "icmp" or protocol == "ipv4":
        json_obj = add_match(json_obj, (icmp_match_template if protocol == "icmp" else ipv4_match_template) % (hostmac1, hostmac2))
        json_obj = add_action(json_obj, action_template % "NORMAL")
    elif protocol == "all":
        op = kwargs["op"]
        if op == 1:
            flow_type = "from"
            match_template = all_from_match_template
        elif op == 2:
            flow_type = "to"
            match_template = all_to_match_template
        else:
            raise Exception("unsupported arp operation code")
        url = f"{ODL_rest_addr}/restconf/config/opendaylight-inventory:nodes/node/openflow:{vSwitch[1:]}/table/0" \
              f"/flow/{vSwitch}-{protocol}-{flow_type}-{hostname1}-{hostname2}"
        json_obj = json.loads(flow_template % (vSwitch, protocol, flow_type, hostname1, hostname2))
        json_obj = add_match(json_obj, match_template % hostmac1)
        json_obj = add_action(json_obj, action_template % "NORMAL")
    else:
        raise Exception("unsupported protocol")
    r = requests.put(auth=("admin", "admin"), json=json_obj, url=url)
    print("enable", protocol, vSwitch, hostname1, hostname2)


def add_match(json_obj, match):
    json_obj['flow']['match'].update(json.loads(match))
    return json_obj


def add_action(json_obj, action):
    json_obj['flow']['instructions']['instruction'][0]['apply-actions']['action'].append(json.loads(action))
    return json_obj


def disable_flow(protocol, vSwitch, hostname1, hostname2, **kwargs):
    url = f"{ODL_rest_addr}/restconf/config/opendaylight-inventory:nodes/node/openflow:{vSwitch[1:]}/table/0" \
          f"/flow/{vSwitch}-{protocol}-all-{hostname1}-{hostname2}"
    if protocol == "arp":
        arp_op = kwargs["op"]
        if arp_op == 1:
            arp_type = "request"
        elif arp_op == 2:
            arp_type = "reply"
        else:
            raise Exception("unsupported arp operation code")
        url = f"{ODL_rest_addr}/restconf/config/opendaylight-inventory:nodes/node/openflow:{vSwitch[1:]}/table/0" \
              f"/flow/{vSwitch}-{protocol}-{arp_type}-{hostname1}-{hostname2}"
    elif protocol == "icmp" or protocol == "ipv4":
        pass
    elif protocol == "all":
        op = kwargs["op"]
        if op == 1:
            flow_type = "from"
        elif op == 2:
            flow_type = "to"
        else:
            raise Exception("unsupported arp operation code")
        url = f"{ODL_rest_addr}/restconf/config/opendaylight-inventory:nodes/node/openflow:{vSwitch[1:]}/table/0" \
              f"/flow/{vSwitch}-{protocol}-{flow_type}-{hostname1}-{hostname2}"
    else:
        raise Exception("unsupported protocol")
    r = requests.delete(auth=("admin", "admin"), url=url)
    print("disable", protocol, vSwitch, hostname1, hostname2)


# enable ARP protocol between host1 and host2, bidirectional
def enable_ARP_reply(hostname1, hostmac1, hostname2, hostmac2):
    for s in ["s1"]:
        enable_flow("arp", s, hostname1, hostmac1, hostname2, hostmac2, op=2)
        enable_flow("arp", s, hostname2, hostmac2, hostname1, hostmac1, op=2)


def disableARP_reply(hostname1, hostname2):
    for s in ["s1"]:
        disable_flow("arp", s, hostname1, hostname2, op=2)
        disable_flow("arp", s, hostname2, hostname1, op=2)


def enableICMPv4(hostname1, hostmac1, hostname2, hostmac2):
    for s in ["s1"]:
        enable_flow("icmp", s, hostname1, hostmac1, hostname2, hostmac2)
        enable_flow("icmp", s, hostname2, hostmac2, hostname1, hostmac1)


def disableICMPv4(hostname1, hostname2):
    for s in ["s1"]:
        disable_flow("icmp", s, hostname1, hostname2)
        disable_flow("icmp", s, hostname2, hostname1)


def enableIPv4(hostname1, hostmac1, hostname2, hostmac2):
    for s in ["s1"]:
        enable_flow("ipv4", s, hostname1, hostmac1, hostname2, hostmac2)
        enable_flow("ipv4", s, hostname2, hostmac2, hostname1, hostmac1)


def disableIPv4(hostname1, hostname2):
    for s in ["s1"]:
        disable_flow("ipv4", s, hostname1, hostname2)
        disable_flow("ipv4", s, hostname2, hostname1)


def publicAC_server(hostname, mac):
    for s in ["s1"]:
        enable_flow("arp", s, None, None, None, None, op=1)
        enable_flow("all", s, hostname, mac, None, None, op=1)
        enable_flow("all", s, hostname, mac, None, None, op=2)
