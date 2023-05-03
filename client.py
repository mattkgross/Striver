import json
import time
from typing import *
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Make sure the
# If you haven't already authorized your app, do so by following this URL:
# https://www.strava.com/oauth/authorize?client_id=your_client_id&redirect_uri=http://localhost&response_type=code&scope=read_all,profile:read_all,activity:read_all
class StravaHttpClient():
  authUrl = "https://www.strava.com/oauth/token"
  getLastActivityEndpoint = "https://www.strava.com/api/v3/athlete/activities"
  getActivityEndpoint = "https://www.strava.com/api/v3/activities/"

  def __init__(self):
    self.__GetConfig()
    self._Authorize()

  ####################
  ## AUTHENTICATION ##
  ####################

  # This reads from a file that should be named 'strava_auth' and placed in the config directory.
  def __GetConfig(self):
    try:
      with open("config/strava_auth.json", "r") as creds:
        self.__config = json.load(creds)
        self.__clientId: str = self.__config["clientId"]
        self.__clientSecret: str = self.__config["clientSecret"]
        self.__refreshToken: str = self.__config["refreshToken"]
    except Exception as e:
      print("Credentials failed to load!")
      raise e
    else:
      print("Credentials loaded.")

  def __SetRefreshToken(self):
    try:
      self.__config["refreshToken"] = self.__refreshToken
      with open("config/strava_auth.json", "w") as creds:
        json.dump(self.__config, creds)
    except Exception as e:
      print("Failed to write refresh token!")
      raise e
    else:
      print("Refresh token saved.")



  def _Authorize(self):
    payload = {
      'client_id': self.__clientId,
      'client_secret': self.__clientSecret,
      'refresh_token': self.__refreshToken,
      'grant_type': "refresh_token",
      'f': 'json'
    }

    print("Requesting Token...")
    res = requests.post(self.authUrl, data=payload, verify=False).json()

    try:
      self.__access_token = res["access_token"]
      self.__accessExpirationUtc = res["expires_at"]
      self.__refreshToken = res["refresh_token"]

      self.__SetRefreshToken()
    except Exception as e:
      print("No access token returned.")
      raise e
    else:
      print ("Auth token acquired.")
      #print (self.__access_token)

  def _Get(self, url: str, params) -> Any:
    # If we're within 10 minutes of access expiration, refresh.
    if self.__accessExpirationUtc < (round(time.time()) - 600):
      print("Access token almost stale. Refreshing...")
      self._Authorize()

    header = {'Authorization': 'Bearer ' + self.__access_token}
    return requests.get(url, headers=header, params=params).json()

  def GetLastActivity(self) -> Any:
    params = {"per_page": 1, 'page': 1}

    # Make the API request.
    activities = self._Get(self.getLastActivityEndpoint, params)
    activity = activities[0] if activities else None

    if activity is None:
      return None

    # Get the full details.
    return self._Get(self.getActivityEndpoint + str(activity["id"]), None)