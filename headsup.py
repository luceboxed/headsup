# imports
from plyer import notification
import json
import requests
import time
import PySimpleGUI as sg
from datetime import datetime
import os, sys

def checkAlerts():
    response_api = requests.get(url + lat + ',' + lon)
    data = response_api.text
    parse_json = json.loads(data)
    try:
            num_alerts = len(parse_json['features'])
    except:
            num_alerts = 0
    print("checking @ " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " - " + str(num_alerts) + " currently active")
    if num_alerts > 0:
        #remove expired alerts
        for i in reversed(range(len(alertcache))):
            if alertcache[i] not in parse_json['features'][i]['properties']['id']:
                print("removing " + alertheadlines[i] + " - expired, cancelled, or updated")
                del alertcache[i]
                del alertheadlines[i]
        for i in range(num_alerts):
            if parse_json['features'][i]['properties']['id'] not in alertcache:
                print("found new " + parse_json['features'][i]['properties']['headline'][:256])
                notification.notify(title="Heads Up! - Check app for more details.", message=parse_json['features'][i]['properties']['headline'][:256], app_name="Heads Up!", ticker="Weather Alert", timeout=10)
                alertcache.append(parse_json['features'][i]['properties']['id'])
                alertheadlines.append(parse_json['features'][i]['properties']['headline'][:256])
                window['Alerts:'].update(alertheadlines)
                window['alertcount'].update("You have " + str(num_alerts) + " alerts in your area.")
            else:
                print("already seen this one - skipping " + parse_json['features'][i]['properties']['event'][:256])

# creates functions for getting coordinates and sleeptime
def get_lat():
    lat = sg.popup_get_text('Please enter your latitude.', 'Heads Up! - Location', default_text='35.155')
    return lat
def get_lon():
    lon = sg.popup_get_text('Please enter your longitude.', 'Heads Up! - Location', default_text='-90.052')
    return lon
def get_sleep():
    sleeptime = int(sg.popup_get_text('How many seconds would you like to wait between checks?', 'Heads Up! - Check Frequency', default_text='60'))
    return sleeptime

# creates function for restarting script
def restart():
    os.execv(sys.executable, [os.path.basename(sys.executable)] + sys.argv)

lat = get_lat()
lon = get_lon()
sleeptime = get_sleep()
url = "https://api.weather.gov/alerts/active?point="
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
frame_layout = [[sg.Text("You have " + str(num_alerts) + " alerts in your area.", key='alertcount')],
            [sg.Text("Alerts:")],
            [sg.Listbox(values=alertheadlines, size=(60, 20), key='Alerts:', enable_events=True)],
            [sg.Button('New'), sg.Button('Exit')]]
layout = [[sg.Frame('Heads Up!', frame_layout, font='Any 18', title_color='red')]]
window = sg.Window('Heads Up! for ' + lat + "," + lon, layout)
cooltime = time.time()
initialcheck = False
while True:
    event, values = window.read(timeout=1000)
    if event == (sg.WIN_CLOSED or 'Exit'):
        break
    #restarts script to input new coordinates
    elif event == 'New':
        restart()

    #show alert details if clicked in listbox
    try:
        if event == 'Alerts:':
            sg.Popup(parse_json['features'][window['Alerts:'].get_indexes()[0]]['properties']['event'] + "\nEffective " + parse_json['features'][window['Alerts:'].get_indexes()[0]]['properties']['onset'] + "\nExpires " + parse_json['features'][window['Alerts:'].get_indexes()[0]]['properties']['expires'] +"\n" + parse_json['features'][window['Alerts:'].get_indexes()[0]]['properties']['description']
            ,title=parse_json['features'][window['Alerts:'].get_indexes()[0]]['properties']['parameters']['NWSheadline'][0], non_blocking=True, keep_on_top=True)
    except:
        sg.Popup("No alert details available or lookup failed.", title="No details", non_blocking=True, keep_on_top=True)
    if initialcheck == False:
        checkAlerts()
        initialcheck = True
    #check alerts every x seconds without using sleep
    if time.time() - cooltime > sleeptime:
        checkAlerts()
        cooltime = time.time()
window.close()
exit()
