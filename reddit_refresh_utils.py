import json, requests

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
        url = "https://api.pushbullet.com/v2/pushes"
        data = {"body": "This is a test.", "title": "Test", "type": \
                "note", "device_iden": device}
        headers = {'Content-Type': 'application/json', 'Access-Token': token}
        data_json = json.dumps(data)
        payload = {"json_payload": data_json}
        result = requests.post(url, data=data_json, headers=headers)

def send_a_push_link(devices_to_push, token, link, title):
    for device in devices_to_push:
        url = "https://api.pushbullet.com/v2/pushes"
        data = {"title": title, "url": link, "type": "link", \
                "device_iden": device}
        headers = {'Content-Type': 'application/json', 'Access-Token': token}
        data_json = json.dumps(data)
        payload = {"json_payload": data_json}
        requests.post(url, data=data_json, headers=headers)
