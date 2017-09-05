import json
import requests

def main():
    token = input("Enter your Pushbullet access token " + \
            "(found on the Account Settings page): ")
    header = 'Access-Token: ' + token
    accinfo = requests.get('https://api.pushbullet.com/v2/users/me', auth=(token, ''))
    out = json.loads(accinfo.text)
    deviceinfo = requests.get('https://api.pushbullet.com/v2/devices', auth=(token, ''))
    device_dict = get_devices(json.loads(deviceinfo.text))
    choice_list = create_choice_list(device_dict)
    get_devices_to_push(choice_list)


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
    print("\nList of devices available to push to: ")
    for i in range(0, len(choice_list)):
        print(str(i) + ":",  choice_list[i][1])
    devices = input("Device numbers you'd like to push to (separate with commas): ")
    numb_list = devices = devices.strip().split(",")
    print(numb_list)


main()
