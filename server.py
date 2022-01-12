# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main
   Description :
   Author :       unstoppable
   date：          4/1/2022
-------------------------------------------------
   Change Activity:
                   4/1/2022:
-------------------------------------------------
"""
import json

from flask import Flask, request

from model import Device, User
from config import device_list, user_list, group_list

devices = [Device(d['devicename'], d['owner'], d['group'], d['permission'], d['mac'], d['ip'])
           for d in device_list]

app = Flask(__name__)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_data()
    auth = json.loads(data)
    user = User(auth["user"], auth["pass"], auth["mac"], auth["ip"])
    if user.auth(user_list):
        for device in devices[1:]:
            device.grant(user)
        return {"status": "ok"}
    else:
        return {"status": "error"}


@app.route("/logout", methods=["POST"])
def logout():
    data = request.get_data()
    auth = json.loads(data)
    user = User(auth["user"], auth["pass"], auth["mac"], auth["ip"])
    if user.auth(user_list):
        for device in devices[1:]:
            device.disallow(user)
        return {"status": "ok"}
    else:
        return {"status": "error"}


if __name__ == '__main__':
    app.run(
        host="10.0.0.1",
        port=80
    )
