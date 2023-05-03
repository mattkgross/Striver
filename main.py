import json
import time
from typing import *

from client import StravaHttpClient

def main():
  stravaClient: StravaHttpClient = StravaHttpClient()
  lastActivityUpdatedId: int = 0

  # Run the program indefinitely
  while True:
    activity: Any = stravaClient.GetLastActivity()
    activityId: int = activity["id"]

    if activityId != lastActivityUpdatedId:
      LastActivityStripHr(activity)
      LastActivityAddPoem(activity)

    lastActivityUpdatedId = activityId

    # Wait for a minute before checking for new data.
    time.sleep(60)

def LastActivityStripHr(activity: Any) -> None:
  #print(json.dumps(activity, indent=4))
  pass

def LastActivityAddPoem(activity: Any) -> None:
  if "description" not in activity:
    # Give it a poem.

if __name__ == "__main__":
  main()