#!/usr/bin/env python3

import json
import requests
import os
from pathlib import Path
from subreddit_parser import get_results

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
        secondline = config.tell()
        #get access token from user and write it to the first line
        token = input("Enter your Pushbullet access token " + \
                "(found on the Account Settings page): ")
        config.write("token=" + token + "\n")
        #close and repon the file for reading and writing
        config.close()
        config = open(str(Path.home())+"/.config/reddit-refresh/config", 'r+')
    #otherwise, get the token and do some formatting
    else:
        #get location of second line of the file for later use
        secondline = config.tell()
        config.seek(0)
        token = config.readline().split('=')[1].strip()
        tmp = config.readline()
        if(tmp == "" or tmp == "\n"):
            config.write("\n")
        config.seek(secondline)
    #get the account info from the Pushbullet API
    accinfo = requests.get('https://api.pushbullet.com/v2/users/me', auth=(token, ''))
    #get the text from the json object
    out = json.loads(accinfo.text)
    #if line with token is the only line in the file
    if('token' in config.readline().strip()):
        #get device info and creates a device dictionary with this info
        deviceinfo = requests.get('https://api.pushbullet.com/v2/devices', auth=(token, ''))
        device_dict = get_devices(json.loads(deviceinfo.text))
        #get a list of tuple objects where each tuple is a key-value pair
        choice_list = create_choice_list(device_dict)
        #get the devices to push using the choice list
        devices_to_push = get_devices_to_push(choice_list)
        #write each device to the config file, using a standard format
        for i in range(len(devices_to_push)):
            if(i == len(devices_to_push)):
                config.write(devices_to_push[i][0] + ",")
                config.write(devices_to_push[i][1])
            else:
                config.write(devices_to_push[i][0] + ",")
                config.write(devices_to_push[i][1] + "\n")
    #if line with token is not the only line in file 
    else:
        #create empty dictionary
        devices_to_push = {}
        #go to second line of the file 
        config.seek(secondline)
        #read in each of the devices
        device = config.readline()
        while(device != "" and device != "\n"):
            device = device.split(",")
            devices_to_push[device[0]] = device[1].strip()
            device = config.readline()
    search_results = get_results("mechmarket", "Planck")
    previous_results = []
    if os.path.isfile(str(Path.home())+"/.config/reddit-refresh/visited_sites.txt"):
        seen = open(str(Path.home())+"/.config/reddit-refresh/visited_sites.txt", 'r+')
        for line in seen:
            previous_results.append(line.strip())
    else:
        seen = open(str(Path.home())+"/.config/reddit-refresh/visited_sites.txt", 'w')
        for key in search_results:
            seen.write(key + "\n")
    noMatches = True
    if(len(previous_results) > 0):
        for key in search_results:
            if key not in previous_results:
                send_a_push_link(devices_to_push, token, \
                        key, search_results[key])
                seen.write(key + "\n")
            else:
                noMatches = False
        if noMatches:
            seen.truncate(0)
            for key in search_results:
                seen.write(key + "\n")
    else:
        for key in search_results:
            send_a_push_link(devices_to_push, token, \
                    key, search_results[key])
            break
    #close file as standard practice
    config.close()
    seen.close()

'''
Create a dictionary of devices where the nickname is mapped to the id
@param deviceout - json device request to get device info from 
@return device_dict - dictionary mapping nickname to the id of each device
'''
def get_devices(deviceout):
    device_dict = {}
    for i in deviceout["devices"]:
       if "nickname" in i and "iden" in i:
           device_dict[i["iden"]] = i["nickname"]
    return device_dict

'''
Takes in the device dict from get_devices() and outputs a list of device choices
@param device_dict - dictionary mapping nickname to the id of each device
@return choice_list - a lists of device choice tuples created from device_dict
'''
def create_choice_list(device_dict):
    choice_list = []
    for i in device_dict:
        choice_list.append((i, device_dict[i]))
    return choice_list
'''
Takes in the choice list, prints the list in a readable format, and prompts 
the user to input which devices they want to push to
@param choice_list - list of device tuple objects to use as options
@return device_list - list of device
'''
def get_devices_to_push(choice_list):
    device_list = []
    print("\nList of devices available to push to: ")
    for i in range(0, len(choice_list)):
        print(str(i) + ":",  choice_list[i][1])
    devices = input("Device numbers you'd like to push to (separate with commas): ")
    numb_list  = devices.strip().split(",")
    for i in numb_list:
        device_list.append(choice_list[int(i)])
    return device_list

def send_a_push_test(devices_to_push, token):
    for device in devices_to_push:
        print(device)
        url = "https://api.pushbullet.com/v2/pushes"
        data = {"body": "This is a test.", "title": "Test", "type": \
                "note", "device_iden": device}
        headers = {'Content-Type': 'application/json', 'Access-Token': token}
        data_json = json.dumps(data)
        payload = {"json_payload": data_json}
        requests.post(url, data=data_json, headers=headers)

def send_a_push_link(devices_to_push, token, link, title):
    for device in devices_to_push:
        url = "https://api.pushbullet.com/v2/pushes"
        data = {"title": title, "url": link, "type": "link", \
                "device_iden": device}
        headers = {'Content-Type': 'application/json', 'Access-Token': token}
        data_json = json.dumps(data)
        payload = {"json_payload": data_json}
        requests.post(url, data=data_json, headers=headers)

main()
