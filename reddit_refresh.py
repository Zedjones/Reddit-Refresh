#!/usr/bin/env python3

import os
from pathlib import Path
from subreddit_parser import get_results
import configparser
import time
from reddit_refresh_utils import *
import platform

def main():
    #assume that this is the first run
    firstrun = True
    #make the directory to hold the config if it doesn't exist
    if(platform.system() == "Windows"):
        home = os.getcwd()
    else:
        try:
            home = str(Path.home())
        except:
            home = os.path.expanduser("~")

    if not os.path.exists(home+"/.config"):
        os.makedirs(home+"/.config")	
    if not os.path.exists(home+"/.config/reddit-refresh"):
        os.makedirs(home+"/.config/reddit-refresh")
    #open the config file for reading and writing if it exists, set firstRun to false
    if os.path.isfile(home+"/.config/reddit-refresh/config"):
        configf = open(home+"/.config/reddit-refresh/config", 'r+')
        firstrun = False
    #otherwise,  open a new config file for writing
    else:
        configf = open(home+"/.config/reddit-refresh/config", 'w')
    #create new config parser
    config = configparser.ConfigParser()
    #read the config file
    config.read(home+"/.config/reddit-refresh/config")
    #if it's the first run or there is no User Info section 
    if(firstrun or "User Info" not in config):
        #get access token from user
        token = input("Enter your Pushbullet access token " + \
                "(found on the Account Settings page): ")
        #set entry in User Info for token to the token provided
        config['User Info'] = {}
        config['User Info']['token'] = token
    #otherwise, get the token from the config file
    else:
        token = config['User Info']['token']
    #get the account info from the Pushbullet API
    accinfo = requests.get('https://api.pushbullet.com/v2/users/me', auth=(token, ''))
    #get the text from the json object
    out = json.loads(accinfo.text)
    #if there is no Devices section in the config file
    if('Devices' not in config):
        #get device info and creates a device dictionary with this info
        deviceinfo = requests.get('https://api.pushbullet.com/v2/devices', auth=(token, ''))
        device_dict = get_devices(json.loads(deviceinfo.text))
        #get a list of tuple objects where each tuple is a key-value pair
        choice_list = create_choice_list(device_dict)
        #get the devices to push using the choice list
        devices_to_push = get_devices_to_push(choice_list)
        #create an entry for each device in the Devices section
        config['Devices'] = {}
        for i in range(len(devices_to_push)):
            config['Devices'][devices_to_push[i][1]] = \
                    devices_to_push[i][0]
        #create empty dictionary
        devices_to_push = {}
        #read each entry in Devices and put it in the dictionary
        for entry in config['Devices']:
            devices_to_push[config['Devices'][entry]] = entry
    #if there is a Devices section
    else:
        #create empty dictionary
        devices_to_push = {}
        #read each entry in Devices and put it in the dictionary
        for entry in config['Devices']:
            devices_to_push[config['Devices'][entry]] = entry
    searches = []
    if('Searches' not in config):
        print("\nHit enter to stop inputting queries")
        search = input("\nEnter the subreddit to search and the search term\n" + \
                "separated by a comma (Ex: mechmarket,Planck): ").split(",")
        config['Searches'] = {}
        while(search[0] != ''):
            if(search[0].strip() in config['Searches']):
                config['Searches'][search[0].strip()] += ",%s" % search[1].strip()
            else:
                config['Searches'][search[0].strip()] = search[1].strip()
            searches.append(search)
            search = input("\nEnter the subreddit to search and the search\n" \
            + "term separated by a comma (Ex: mechmarket,Planck): ").split(",")
    else:
        for entry in config['Searches']:
            for term in config['Searches'][entry].split(','):
                search = []
                search.append(entry.strip())
                search.append(term.strip())
                searches.append(search)
    if('Program Config' not in config):
        minutes = input("How often should the program check for new" \
               + " results? (in minutes): ")
        config['Program Config'] = {}
        config['Program Config']['refresh interval'] = minutes
    else:
        minutes = config['Program Config']['refresh interval']
    print("CTRL-C to exit program and stop checking results")
    while(1):
        print("checking results")
        for search in searches:
            search_results = get_results(search[0], search[1], "new")
            previous_results = []
            #create list to hold the previous results
            #if visited_sites is a file, open it for reading and writing
            if os.path.isfile(home+"/.config/reddit-refresh/%s_%s" \
                % (search[0], search[1] + "_visited_sites.txt")):
                seen = open(home+"/.config/reddit-refresh/%s_%s" \
                    % (search[0], search[1]) + "_visited_sites.txt", 'r+')
                #for each url in the file
                for line in seen:
                    #add it to the list
                    previous_results.append(line.strip())
            #if it is not a file, create the file and open it for writing
            else:
                seen = open(home+"/.config/reddit-refresh/%s_%s" \
                    % (search[0], search[1]) + "_visited_sites.txt", 'w')
                #write each url to the file, close it, and reopen it for r+w
                i = 0
                for key in search_results:
                    seen.write(key + "\n")
                    i += 1
                    if(i == 2):
                    	break
                seen.close()
                seen = open(home+"/.config/reddit-refresh/%s_%s" \
                    % (search[0], search[1]) + "_visited_sites.txt", 'r+')
            noMatches = True
            #if there were any previous results
            if(len(previous_results) != 0):
                #only send a push if a result hasn't been seen before, and then 
                #write the url to the file
                line = 1
                seen.seek(0)
                for key in search_results:
                    if key not in previous_results:
                        send_a_push_link(devices_to_push, token, \
                                key, search_results[key])
                        seen.write(key + "\n")
                        seen.write(previous_results[0])
                        if(line == 2):
                            seen.seek(0)
                        else:
                            line += 1
                    else:
                        break
            #if there were no previous results, just send the first result
            else:
                for key in search_results:
                    send_a_push_link(devices_to_push, token, \
                            key, search_results[key])
                    break
        #close file as standard practice, and write config to file
        if not configf.closed:
            config.write(configf)
            configf.close()
        seen.close()
        time.sleep(float(minutes)*60)

main()
