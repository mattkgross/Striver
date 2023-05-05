import time
from typing import *

import requests

from client import StravaHttpClient

## Functionality Options ##
RunLastActivityStripHr = True
RunLastActivityAddPoem = True

def main():
  stravaClient: StravaHttpClient = StravaHttpClient()
  lastActivityUpdatedId: int = 0

  # Run the program indefinitely
  while True:
    activity: Any = stravaClient.GetLastActivity()
    activityId: int = activity["id"]

    if activityId != lastActivityUpdatedId:
      if RunLastActivityStripHr:
        LastActivityStripHr(stravaClient, activity)
      if RunLastActivityAddPoem:
        LastActivityAddPoem(stravaClient, activity)

    lastActivityUpdatedId = activityId

    # Wait for a minute before checking for new data.
    time.sleep(60)

def LastActivityStripHr(client: StravaHttpClient, activity: Any) -> None:
  print(f"Removing HR data from AcivityId {activity['id']}")
  print(f"{activity['name']} @ {activity['start_date_local']}")
  res = client.RemoveHeartRate(activity["id"])

  if res.status_code == 200:
    print("HR hidden.")
  else:
    print("Failed to hide HR.")

def LastActivityAddPoem(client: StravaHttpClient, activity: Any) -> None:
  if "description" not in activity:
    # Give it a poem.
    pass

if __name__ == "__main__":
  main()