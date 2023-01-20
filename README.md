# Heads Up!
Up-to-date watch, warning, and advisory messages for a selected location using the National Weather Service [API](https://api.weather.gov/).

*Very much still a work in progress, sorry for messy code!*

## Current Features

- Choose a coordinate to watch for alerts
- Pushes a notification if a new alert is found (not tested on macOS)
- Customize the time between checking for new alerts
- Click on an alert in the app for more details

## Prerequisites

You will need the latest version of [Python](https://www.python.org/downloads/) installed.

To install the required packages, run this command in your terminal.
```
pip install -r /path_here/headsup/requirements.txt
```

## Known Issues

macOS has not been tested, but notifications are expected to work properly.

Improper coordinates cause the app to crash.

## Screenshots

![A picture of the Heads Up! app, showing its terminal and app. The app displays 2 Avalanche Warnings and a Winter Storm Watch. The Winter Storm Watch is selected and additional info is on screen. A notification about the Avalanche Warning can be seen in the corner.](https://raw.githubusercontent.com/spikeyscout/headsup/2b2ad11f2dc583d69bde8a0b6c8b356fc77b4a82/img/img1.png)
![A picture of the Heads Up! app, running on Linux.](https://github.com/spikeyscout/headsup/blob/main/img/img2.png?raw=true)
