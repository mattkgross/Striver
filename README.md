> *A set of Strava utilities that you can run on a home server.*

# Features
You can toggle features within `src/config/feature_switches.py`.

## Hide Latest Activity Heart Rate
Hides your latest activity's heart rate data (you can still see it).

## Poetry
If your latest activity has no description, fill it with a random quote.

## Equipment Select
If you specified equipment defaults for activity types, updates your last activity's data accordingly.

Map equipment in `src/config/equipment.py` - you'll need to lookup your gear IDs. It should look something like this:

```
EquipmentMap = {
  "gear":
  {
    "hiking_shoes": "g10352053",
    "road_runners": "g12945572",
    "trail_runners": "g12776882"
  },
  "sportTypes":
  {
    "Walk": "hiking_shoes",
    "Hike": "hiking_shoes",
    "Run": "road_runners",
    "TrailRun": "trail_runners"
  }
}
```

Give each of your gear an nickname as it's key in `gear`. Then, specify which piece of gear should be the default for a particular activity sport type in `sportTypes`.

# Setup

## Running
This is built with python3. No guarantees it'll work on python2.

```
python3 main.py
```

## Secrets
You'll need to create a file under the `config` directory named `strava_auth.json`. Its contents should look as follows:

```
{
  "clientId": "your strava app's client ID",
  "clientSecret": "your app's client secret",
  "refreshToken": "your current refresh token"
}
```

## Getting a Refresh Token
Strava uses refresh tokens in order to generate short-lived auth tokens. To get one yourself, you'll first need to have a [registered application under your Strava account](https://www.strava.com/settings/api).

Once you've got your app registered, visit `https://www.strava.com/oauth/authorize?client_id=your_client_id&redirect_uri=http://localhost&response_type=code&scope=read_all,profile:read_all,profile:write,activity:read_all,activity:write`, inserting your own client id into the URL.

This will redirect you back to localahost with a `code` param in the URL. Copy this code and send a POST request to `https://www.strava.com/oauth/token?client_id=your_client_id&client_secret=your_client_secret&code=the_code_you_copied&grant_type=authorization_code`, which will return to you both a current authorization token, as well as a refresh token. Copy your client id, client secret, and refresh token to the file above as described.

**Remember, once you use a refresh token to generate a new auth/refresh token pair, it's no longer valid. So, if you do this elsewhere outside of this app, you'll need to update it accordingly here with the most recent refresh token. If you don't mess with things anywhere else, you'll be fine - this code will automatically generate and save refresh tokens for you after you've generated the first one.**

## On Linux Startup
You can configure this script to start on system boot for Linux systems with `systemctl` following these steps:

1. `sudo vim /etc/systemd/system/striver.service`
2.
```
[Unit]
Description=Strava Utilities Client
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/repo/src/main.py
WorkingDirectory=/path/to/repo
Restart=always
RestartSec=60
User=<your_username>

[Install]
WantedBy=default.target
```
3. `sudo systemctl daemon-reload`
4. `sudo systemctl enable striver.service`
5. `sudo systemctl start striver.service`

To check the service status at any time, run: `sudo systemctl status striver.service`

To restart the service after making changes, run : `sudo systemctl restart striver.service`

## Logs
To check server logs, run: `tail src/striver.log -n 50`

To check systemctl logs, run: `sudo journalctl -u striver.service -n 50`
