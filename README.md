> *A set of Strava utilities that you can run on a home server.*

# Running
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

# Features
You can toggle features within `config/feature_switches.py`.

## Hide Latest Activity Heart Rate
Hides your latest activity's heart rate data (you can still see it).

## Poetry
If your latest activity has no description, fill it with a random quote.

## Equipment Select
If you specified equipment defaults for activity types, updates your last activity's data accordingly. Map equipment in `config/equipment.json` - you'll need to lookup your gear IDs. It should look something like this:

```
{
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