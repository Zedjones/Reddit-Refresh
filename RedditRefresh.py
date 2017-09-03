import json
import requests

def main():
    token = input("Enter your Pushbullet access token " + \
            "(found on the Account Settings page): ")
    header = 'Access-Token: ' + token
    res = requests.get('https://api.pushbullet.com/v2/users/me', auth=(token, ''))
    print(res.text)


main()
