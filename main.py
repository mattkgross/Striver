import json
import time
from clients.quote_client import QuoteHttpClient
from clients.strava_client import StravaHttpClient
from typing import *

## Functionality Options ##
RunLastActivityStripHr = True
RunLastActivityAddPoem = True
RunLastActivityEquipment = True

def main():
  stravaClient: StravaHttpClient = StravaHttpClient()
  quoteClient: QuoteHttpClient = QuoteHttpClient()
  lastActivityUpdatedId: int = 0

  # Run the program indefinitely
  while True:
    activity: Any = stravaClient.GetLastActivity()
    activityId: int = activity["id"]

    if activityId != lastActivityUpdatedId:
      # TODO: These can all be done with a single update call.
      if RunLastActivityStripHr:
        LastActivityStripHr(stravaClient, activity)
      if RunLastActivityAddPoem:
        LastActivityAddPoem(quoteClient, activity)
      if RunLastActivityEquipment:
        LastActivityEquipment(stravaClient, activity)

    lastActivityUpdatedId = activityId

    # Wait for a minute before checking for new data.
    time.sleep(60)

def LastActivityStripHr(client: StravaHttpClient, activity: Any) -> None:
  print(f"Removing HR data from AcivityId {activity['id']}")
  print(f"{activity['name']} @ {activity['start_date_local']}")
  hideHr = "{'heartrate_opt_out': true}"
  res = client.UpdateActivity(activity["id"], hideHr)

  if res.status_code == 200:
    print("HR hidden.")
  else:
    print("Failed to hide HR.")

def LastActivityAddPoem(client: QuoteHttpClient, activity: Any) -> None:
  if "description" not in activity:
    # Give it a poem.
    print(client.GetRandomQuote())

def LastActivityEquipment(client: StravaHttpClient, activity: Any) -> None:
  gearDict = None

  try:
    with open("config/equipment.json", "r") as equipment:
      gearDict = json.load(equipment)
  except Exception as e:
    print("Failed to read equipment list.")
    raise e

  # If the activity is a type we have default gear for, then we set the gear.
  if activity["sport_type"] in gearDict["sportTypes"]:
    gearId = gearDict["gear"][gearDict["sportTypes"][activity["sport_type"]]]
    gearMeta = f"{'gear_id': '{gearId}'}"
    res = client.UpdateActivity(activity["id"], gearMeta)

    if res.status_code == 200:
      print(f"Gear updated for activity {activity['id']}.")
    else:
      print(f"Failed to update gear for activity {activity['id']}.")

if __name__ == "__main__":
  main()