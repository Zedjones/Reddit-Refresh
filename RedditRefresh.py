#!/usr/bin/env python3

import json
import requests
import os
from pathlib import Path

def main():
    firstrun = True
    if not os.path.exists(str(Path.home())+"/.config/reddit-refresh"):
        os.makedirs(str(Path.home())+"/.config/reddit-refresh")
    if os.path.isfile(str(Path.home())+"/.config/reddit-refresh/config"):
        config = open(str(Path.home())+"/.config/reddit-refresh/config", 'r+')
        firstrun = False
    else:
        config = open(str(Path.home())+"/.config/reddit-refresh/config", 'w')
    if(firstrun or "token" not in config.readline()):
        token = input("Enter your Pushbullet access token " + \
                "(found on the Account Settings page): ")
        config.write("token=" + token + "\n")
        config.close()
        config = open(str(Path.home())+"/.config/reddit-refresh/config", 'r+')
    else:
        config.seek(0)
        token = config.readline().split('=')[1].strip()
        tmp = config.readline()
        if(tmp == "" or tmp == "\n"):
            config.write("\n")
        config.seek(0)
        config.readline()
    header = 'Access-Token: ' + token
    accinfo = requests.get('https://api.pushbullet.com/v2/users/me', auth=(token, ''))
    out = json.loads(accinfo.text)
    if('token' in config.readline().strip()):
        deviceinfo = requests.get('https://api.pushbullet.com/v2/devices', auth=(token, ''))
        device_dict = get_devices(json.loads(deviceinfo.text))
        choice_list = create_choice_list(device_dict)
        devices_to_push = get_devices_to_push(choice_list)
        for i in range(len(devices_to_push)):
            if(i == len(devices_to_push)):
                config.write(devices_to_push[i][0] + ",")
                config.write(devices_to_push[i][1])
            else:
                config.write(devices_to_push[i][0] + ",")
                config.write(devices_to_push[i][1] + "\n")
    else:
        devices_to_push = {}
        config.seek(0)
        config.readline()
        device = config.readline()
        while(device != "" and device != "\n"):
            device = device.split(",")
            devices_to_push[device[0]] = device[1].strip()
            device = config.readline()
        print(devices_to_push, token)

def get_devices(deviceout):
    device_dict = {}
    for i in deviceout["devices"]:
       if "nickname" in i and "iden" in i:
           device_dict[i["iden"]] = i["nickname"]
    return device_dict

def create_choice_list(device_dict):
    choice_list = []
    for i in device_dict:
        choice_list.append((i, device_dict[i]))
    return choice_list

def get_devices_to_push(choice_list):
    device_list = []
    print("\nList of devices available to push to: ")
    for i in range(0, len(choice_list)):
        print(str(i) + ":",  choice_list[i][1])
    devices = input("Device numbers you'd like to push to (separate with commas): ")
    numb_list  = devices.strip().split(",")
    for i in numb_list:
        device_list.append(choice_list[int(i)])
    print(device_list)
    return device_list

def send_a_push(devices_to_push, token):
    for device in devices_to_push:
        data = {"body": "This is a test.", "title": "Test", "type": "note"}
        data_json = json.dumps(data)
        payload = {"json_payload": data_json, "Access-Token": token}
        requests.get("https://api.pushbullet.com/v2/devices", data=payload)

main()
