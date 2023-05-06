import json
import time
from typing import *
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class StravaHttpClient():
  """An HTTP client to make requests to the Strava API."""

  AuthUrl: str = "https://www.strava.com/oauth/token"
  GetActivityEndpoint: str = "https://www.strava.com/api/v3/activities/"
  GetLastActivityEndpoint: str = "https://www.strava.com/api/v3/athlete/activities"
  UpdateActivityEndpoint: str = "https://www.strava.com/api/v3/activities/"

  def __init__(self):
    self.__config: dict[str, Any] = {}
    self.__clientId: str = ""
    self.__clientSecret: str = ""
    self.__refreshToken: str = ""
    self.__access_token: str = ""
    self.__accessExpirationUtc: int = 0
    self.__refreshToken: str = ""

    self.__GetConfig()
    self._Authorize(False)

  def __GetConfig(self) -> None:
    """Loads the `config/strava_auth.json` file into memory."""

    try:
      with open("config/strava_auth.json", "r") as creds:
        self.__config = json.load(creds)
        self.__clientId = self.__config["clientId"]
        self.__clientSecret = self.__config["clientSecret"]
        self.__refreshToken = self.__config["refreshToken"]
    except Exception as e:
      print("Credentials failed to load!")
      raise e
    else:
      print("Credentials loaded.")

  def __SetRefreshToken(self) -> None:
    """Persists the current refresh token to `config/strava_auth.json`."""

    try:
      self.__config["refreshToken"] = self.__refreshToken
      with open("config/strava_auth.json", "w") as creds:
        json.dump(self.__config, creds)
    except Exception as e:
      print("Failed to write refresh token!")
    else:
      print("Refresh token saved.")

  def _Authorize(self, refresh: bool = True) -> None:
    """
    Requests the current authorization token for API calls.

    Args:
      refresh (bool): If this call should only be made if it's time to refresh.
    """

    # If this is a refresh and the expiration time is more than 10 mins away, skip.
    if refresh and (self.__accessExpirationUtc - round(time.time())) > 600:
      return

    payload = {
      'client_id': self.__clientId,
      'client_secret': self.__clientSecret,
      'refresh_token': self.__refreshToken,
      'grant_type': "refresh_token",
      'f': 'json'
    }

    print("Requesting Auth Token...")
    res = requests.post(self.AuthUrl, data=payload, verify=False).json()

    try:
      self.__access_token = res["access_token"]
      self.__accessExpirationUtc = res["expires_at"]
      self.__refreshToken = res["refresh_token"]

      self.__SetRefreshToken()
    except Exception as e:
      print("No access token returned. Subsequent calls will fail.")
      # Force a retry on the next call.
      self.__accessExpirationUtc = 0
    else:
      print ("Auth token acquired.")
      # For debug.
      print (self.__access_token)

  def _Get(self, url: str, params) -> Any:
    """
    Performs a GET request to the specified URL with the Strava auth token and specified URL parameters.

    Args:
      url (str): The full API endpoint URL to send the request.
      params (_Params): The query parameters.

    Returns:
      Any: The HTTP response parsed as JSON.
    """
    self._Authorize()

    header = {'Authorization': 'Bearer ' + self.__access_token}
    return requests.get(url, headers=header, params=params).json()

  def _Put(self, url: str, body: dict[str, Any]):
    """
    Performs a PUT request to the specified URL with the Strava auth token and specified body.

    Args:
      url (str): The full API endpoint URL to send the request.
      body (dict[str, Any]): The request body that will be serialized to JSON.

    Returns:
      Any: The HTTP response.
    """
    self._Authorize()

    header = {'Authorization': 'Bearer ' + self.__access_token}
    return requests.put(url, headers=header, json=body)

  def GetLastActivity(self) -> Any:
    """
    Gets the last activity published by the user.

    Returns:
      JSON representation of the activity.
    """
    params = {"per_page": 1, 'page': 1}

    # Make the API request.
    activities = self._Get(self.GetLastActivityEndpoint, params)
    activity = activities[0] if activities else None

    if activity is None:
      return None

    # Get the full details.
    return self._Get(self.GetActivityEndpoint + str(activity["id"]), params)

  def UpdateActivity(self, activityId: int, body: dict[str, Any]) -> Any:
    """
    Updates the specified elements of an existing activity.

    Args:
      activityId (int): The ID of the activity to modify.
      body (dict[str, Any]): The JSON body containing the keys to update with their values.

    Returns:
      Any: The HTTP response.
    """
    return self._Put(self.UpdateActivityEndpoint + str(activityId), body)