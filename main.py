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
        LastActivityAddPoem(stravaClient, quoteClient, activity)
      if RunLastActivityEquipment:
        LastActivityEquipment(stravaClient, activity)

    lastActivityUpdatedId = activityId

    # Wait for a minute before checking for new data.
    time.sleep(60)

def LastActivityStripHr(client: StravaHttpClient, activity: Any) -> None:
  hideHr = "{'heartrate_opt_out': true}"
  res = client.UpdateActivity(activity["id"], hideHr)

  if res.status_code == 200:
    print(f"HR hidden for AcivityId {activity['id']}: {activity['name']} @ {activity['start_date_local']}")
  else:
    print("Failed to hide HR for AcivityId {activity['id']}: {activity['name']} @ {activity['start_date_local']}")

def LastActivityAddPoem(sClient: StravaHttpClient, qClient: QuoteHttpClient, activity: Any) -> None:
  if "description" not in activity:
    # Give it a poem.
    quote = qClient.GetRandomQuote()
    quoteText = f"{quote['content']}\n - {quote['author']}"
    desc = f"{'description': '{quoteText}'}"
    res = sClient.UpdateActivity(activity["id"], desc)

    if res.status_code == 200:
      print(f"Quote generated for activity {activity['id']}.")
    else:
      print(f"Failed to generate quote for activity {activity['id']}.")

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