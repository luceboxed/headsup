# imports
from plyer import notification
import json
import requests
import time

url = "https://api.weather.gov/alerts/active?point="
lat = input("Please enter the latitude of your location.\n> ")
lon = input("Please enter the longitude of your location.\n> ")
sleeptime = int(input("How many seconds would you like to wait between checks?\n> "))
alertcache = []
response_api = requests.get(url + lat + ',' + lon)
print(str(response_api))
print(url + lat + ',' + lon)
data = response_api.text
parse_json = json.loads(data)
num_alerts = len(parse_json['features'])
print(num_alerts)
print(parse_json['title'])
while True:
    for i in range(num_alerts):
        if parse_json['features'][i]['properties']['id'] not in alertcache:
            print(parse_json['features'][i]['properties']['headline'][:256])
            print(parse_json['features'][i]['properties']['description'])
            notification.notify(title="Heads Up! - Check app for more details.", message=parse_json['features'][i]['properties']['headline'][:256], app_name="Heads Up!", ticker="Weather Alert", timeout=10)
            alertcache.append(parse_json['features'][i]['properties']['id'])
    print(alertcache)
    print("checking for new alerts in " + str(sleeptime) + " seconds...")
    time.sleep(sleeptime)