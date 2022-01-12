# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     user.py
   Description :
   Author :       unstoppable
   date：          4/1/2022
-------------------------------------------------
   Change Activity:
                   4/1/2022:
-------------------------------------------------
"""
import sys

sys.path.append("..")
from AC.tool import *


class Host:

    def __init__(self, mac=None, ip=None):
        self.mac = mac
        self.ip = ip
        self.hostname = None


class User(Host):

    def __init__(self, username, password, mac, ip, groups=None):
        Host.__init__(self, mac, ip)
        self.hostname = username
        self.username = username
        self.password = password
        self.groups = groups
        self.verified = False

    def auth(self, user_list):
        for u in user_list:
            if self.username == u['username'] and self.password == u['password']:
                self.groups = u['groups']
                self.verified = True
        return self.verified


class Device(Host):

    def __init__(self, devicename, owner, group, permission, mac, ip):
        Host.__init__(self, mac, ip)
        self.hostname = devicename
        self.devicename = devicename
        self.owner = owner
        self.group = group
        self.permission = permission
        if self.devicename == "AC_server":
            publicAC_server(self.hostname, self.mac)

    def _grant_level(self, user: User, level):
        if level == '0':
            setACL0(device=self, user=user)
        elif level == '1':
            setACL1(device=self, user=user)
        elif level == '2':
            setACL2(device=self, user=user)

    def grant(self, user: User):
        if user.username == "root":
            self._grant_level(user, '2')
        else:
            if self.owner == user.username:
                self._grant_level(user, self.permission[0])
            elif self.group in user.groups:
                self._grant_level(user, self.permission[1])
            else:
                self._grant_level(user, self.permission[2])

    def disallow(self, user: User):
        self._grant_level(user, '0')


# set access control level 0, no match rule
def setACL0(device, user):
    disableARP_reply(device.hostname, user.hostname)
    disableICMPv4(device.hostname, user.hostname)
    disableIPv4(device.hostname, user.hostname)


# set access control level 1, enabling ARP and ICMPv4
def setACL1(device, user):
    setACL0(device, user)
    enable_ARP_reply(device.hostname, device.mac, user.hostname, user.mac)
    enableICMPv4(device.hostname, device.mac, user.hostname, user.mac)


def setACL2(device, user):
    setACL0(device, user)
    enable_ARP_reply(device.hostname, device.mac, user.hostname, user.mac)
    enableIPv4(device.hostname, device.mac, user.hostname, user.mac)
