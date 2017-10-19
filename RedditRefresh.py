#!/usr/bin/env python3

import json
import requests
import os
from pathlib import Path

def main():
    #assume that this is the first run
    firstrun = True
    #make the directory to hold the config if it doesn't exist
    if not os.path.exists(str(Path.home())+"/.config/reddit-refresh"):
        os.makedirs(str(Path.home())+"/.config/reddit-refresh")
    #open the config file for reading and writing if it exists, set firstRun to false
    if os.path.isfile(str(Path.home())+"/.config/reddit-refresh/config"):
        config = open(str(Path.home())+"/.config/reddit-refresh/config", 'r+')
        firstrun = False
    #otherwise,  open a new config file for writing
    else:
        config = open(str(Path.home())+"/.config/reddit-refresh/config", 'w')
    #if it's the firstrun or the config file is malformed
    if(firstrun or "token" not in config.readline()):
        #get access token from user and write it to the first line
        token = input("Enter your Pushbullet access token " + \
                "(found on the Account Settings page): ")
        config.write("token=" + token + "\n")
        #close and repon the file for reading and writing
        config.close()
        config = open(str(Path.home())+"/.config/reddit-refresh/config", 'r+')
    #otherwise, get the token and do some formatting
    else:
        config.seek(0)
        token = config.readline().split('=')[1].strip()
        tmp = config.readline()
        if(tmp == "" or tmp == "\n"):
            config.write("\n")
        config.seek(0)
        config.readline()
    #get the account info from the Pushbullet API
    accinfo = requests.get('https://api.pushbullet.com/v2/users/me', auth=(token, ''))
    #get the text from the json object
    out = json.loads(accinfo.text)
    #if line with token is the only line in the file
    if('token' in config.readline().strip()):
        #get device info and create a device dictionary and choice list
        deviceinfo = requests.get('https://api.pushbullet.com/v2/devices', auth=(token, ''))
        device_dict = get_devices(json.loads(deviceinfo.text))
        choice_list = create_choice_list(device_dict)
        #get the devices to push using the choice list
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
    send_a_push(devices_to_push, token)

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
        print(device)
        url = "https://api.pushbullet.com/v2/pushes"
        data = {"body": "This is a test.", "title": "Test", "type": "note", "device_iden": device}
        headers = {'Content-Type': 'application/json', 'Access-Token': token}
        data_json = json.dumps(data)
        payload = {"json_payload": data_json}
        requests.post(url, data=data_json, headers=headers)

main()
