# imports
from plyer import notification
import json
import requests
import time
import PySimpleGUI as sg

def checkAlerts():
    try:
            num_alerts = len(parse_json['features'])
    except:
            num_alerts = 0
    print(num_alerts)
    if num_alerts > 0:
        for i in range(num_alerts):
            if parse_json['features'][i]['properties']['id'] not in alertcache:
                print(parse_json['features'][i]['properties']['headline'][:256])
                print(parse_json['features'][i]['properties']['description'])
                notification.notify(title="Heads Up! - Check app for more details.", message=parse_json['features'][i]['properties']['headline'][:256], app_name="Heads Up!", ticker="Weather Alert", timeout=10)
                alertcache.append(parse_json['features'][i]['properties']['id'])
                alertheadlines.append(parse_json['features'][i]['properties']['headline'][:256])
                window['Alerts:'].update(alertheadlines)
            else:
                print("already seen this one - skipping")

url = "https://api.weather.gov/alerts/active?point="
lat = input("Please enter the latitude of your location.\n> ")
lon = input("Please enter the longitude of your location.\n> ")
sleeptime = int(input("How many seconds would you like to wait between checks?\n> "))
alertcache = []
alertheadlines = []
response_api = requests.get(url + lat + ',' + lon)
print(str(response_api))
print(url + lat + ',' + lon)
data = response_api.text
parse_json = json.loads(data)
try:
    num_alerts = len(parse_json['features'])
except:
    num_alerts = 0
print(num_alerts)
print(parse_json['title'])

# GUI
layout = [[sg.Text("Heads Up!")],
            [sg.Text("You have " + str(num_alerts) + " alerts in your area.")],
            [sg.Text("Alerts:")],
            [sg.Listbox(values=alertheadlines, size=(60, 20), key='Alerts:', enable_events=True)],
            [sg.Button('Exit')]]
window = sg.Window('Heads Up!', layout)
cooltime = time.time()
initialcheck = False
while True:
    event, values = window.read(timeout=1000)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    #show alert details if clicked in listbox
    if event == 'Alerts:':
        sg.Popup(parse_json['features'][window['Alerts:'].get_indexes()[0]]['properties']['description'], title=parse_json['features'][window['Alerts:'].get_indexes()[0]]['properties']['parameters']['NWSheadline'][0], non_blocking=True, keep_on_top=True)
    if initialcheck == False:
        checkAlerts()
        initialcheck = True
    #check alerts every x seconds without using sleep
    if time.time() - cooltime > sleeptime:
        checkAlerts()
        cooltime = time.time()
window.close()
exit()