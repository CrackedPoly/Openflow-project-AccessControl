# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test.py
   Description :
   Author :       unstoppable
   date：          5/1/2022
-------------------------------------------------
   Change Activity:
                   5/1/2022:
-------------------------------------------------
"""
from config import device_list
from model import User, Device, setACL0, setACL1, setACL2

if __name__ == '__main__':
    devices = [Device(d['devicename'], d['owner'], d['group'], d['permission'], d['mac'], d['ip'])
               for d in device_list]

    setACL1(devices[2], devices[1])
