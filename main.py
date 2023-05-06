import json
import time
from clients.quote_client import QuoteHttpClient
from clients.strava_client import StravaHttpClient
from feature_switches import *
from typing import *

def main():
  stravaClient: StravaHttpClient = StravaHttpClient()
  quoteClient: QuoteHttpClient = QuoteHttpClient()
  lastActivityUpdatedId: int = 0

  # Run the program indefinitely.
  while True:
    activity: Any = stravaClient.GetLastActivity()
    activityId: int = activity["id"]

    if activityId != lastActivityUpdatedId:
      hrCmd = {}
      quoteCmd = {}
      equipmentCmd = {}
      cmd = {}

      if RunLastActivityHideHr:
        hrCmd = LastActivityStripHr(stravaClient, activity)
      if RunLastActivityAddQuote:
        quoteCmd = LastActivityAddQuote(stravaClient, quoteClient, activity)
      if RunLastActivityEquipment:
        equipmentCmd = LastActivityEquipment(stravaClient, activity)

      cmd.update(hrCmd)
      cmd.update(quoteCmd)
      cmd.update(equipmentCmd)

      # If any command keys are present, send the update.
      if bool(cmd):
        res = stravaClient.UpdateActivity(activityId, cmd)

        if res.status_code == 200:
          if bool(hrCmd):
            print(f"HR hidden for AcivityId {activity['id']}: {activity['name']} @ {activity['start_date_local']}")
          if bool(quoteCmd):
            print(f"Quote generated for activity {activity['id']}.")
          if bool(equipmentCmd):
            print(f"Gear updated for activity {activity['id']}.")
        else:
          if bool(hrCmd):
            print("Failed to hide HR for AcivityId {activity['id']}: {activity['name']} @ {activity['start_date_local']}")
          if bool(quoteCmd):
            print(f"Failed to generate quote for activity {activity['id']}.")
          if bool(equipmentCmd):
            print(f"Failed to update gear for activity {activity['id']}.")

      lastActivityUpdatedId = activityId

    # Wait for a minute before checking for new data.
    time.sleep(60)

def LastActivityStripHr(client: StravaHttpClient, activity: Any) -> dict[str, str]:
  return { "heartrate_opt_out": True }

def LastActivityAddQuote(sClient: StravaHttpClient, qClient: QuoteHttpClient, activity: Any) -> dict[str, str]:
  if activity["description"] is None:
    quote = qClient.GetRandomQuote()
    quoteText = f"{quote['content']}\n - {quote['author']}"
    return { "description": quoteText }
  return {}

def LastActivityEquipment(client: StravaHttpClient, activity: Any) -> str:
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
    return { "gear_id": gearId }
  return {}

if __name__ == "__main__":
  main()