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


def get_devices(deviceout):
    device_dict = {}
    for i in deviceout["devices"]:
       if "nickname" in i and "iden" in i:
           device_dict[i["iden"]] = i["nickname"]
    return device_dict
           


main()
