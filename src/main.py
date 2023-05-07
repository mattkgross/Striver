import logging
import logging.handlers
import time
from clients.quote_client import QuoteHttpClient
from clients.strava_client import StravaHttpClient
from config.equipment import *
from config.feature_switches import *
from config.logging import *
from typing import *

_logger = logging.getLogger(__name__)

def main():
  __SetupLogs()

  stravaClient: StravaHttpClient = StravaHttpClient()
  quoteClient: QuoteHttpClient = QuoteHttpClient()
  lastActivityUpdatedId: int = 0

  # TODO: Consider webhooks if we're constantly exceeding API limits: https://developers.strava.com/docs/webhooks/
  # Run the program indefinitely.
  while True:
    lastActivityId = stravaClient.GetLastActivityId()

    if lastActivityId == 0:
      _logger.warning("No activity ID was found. Skipping...")
      time.sleep(60)
      continue

    # Perform operations on the last activity registered.
    if lastActivityId != lastActivityUpdatedId:
      activity = stravaClient.GetActivity(lastActivityId)

      if activity is None:
        _logger.warning("No activity was found. Skipping...")
        time.sleep(60)
        continue

      UpdateLastActivity(activity, stravaClient, quoteClient)
      lastActivityUpdatedId = lastActivityId

    # Wait for a minute before checking for new data.
    time.sleep(60)

def UpdateLastActivity(activity: Any, stravaClient: StravaHttpClient, quoteClient: QuoteHttpClient) -> int:
  hrCmd: dict[str, str] = {}
  quoteCmd: dict[str, str] = {}
  equipmentCmd: dict[str, str] = {}
  cmd: dict[str, Any] = {}
  activityId: int = activity["id"]

  if RUN_LAST_ACTIVITY_HIDE_HR:
    hrCmd = { "heartrate_opt_out": True }
  if RUN_LAST_ACTIVITY_ADD_QUOTE:
    quoteCmd = __LastActivityAddQuoteCmd(stravaClient, quoteClient, activity)
  if RUN_LAST_ACTIVITY_EQUIPMENT:
    equipmentCmd = __LastActivityAddEquipmentCmd(stravaClient, activity)

  cmd.update(hrCmd)
  cmd.update(quoteCmd)
  cmd.update(equipmentCmd)

  # If any command keys are present, send the update.
  if bool(cmd):
    res = stravaClient.UpdateActivity(activityId, cmd)

    if res.status_code == 200:
      if bool(hrCmd):
        _logger.info(f"HR hidden for AcivityId {activity['id']}: {activity['name']} @ {activity['start_date_local']}")
      if bool(quoteCmd):
        _logger.info(f"Quote assigned to activity {activity['id']}.")
      if bool(equipmentCmd):
        _logger.info(f"Gear updated for activity {activity['id']}.")
    else:
      if bool(hrCmd):
        _logger.warning("Failed to hide HR for AcivityId {activity['id']}: {activity['name']} @ {activity['start_date_local']}")
      if bool(quoteCmd):
        _logger.warning(f"Failed to assign quote to activity {activity['id']}.")
      if bool(equipmentCmd):
        _logger.warning(f"Failed to update gear for activity {activity['id']}.")

def __LastActivityAddQuoteCmd(sClient: StravaHttpClient, qClient: QuoteHttpClient, activity: Any) -> dict[str, str]:
  if activity["description"] is None:
    try:
      quote = qClient.GetRandomQuote()
      quoteText = f"{quote['content']}\n - {quote['author']}"
      return { "description": quoteText }
    except Exception as e:
      _logger.warning("Failed to retrieve quote.")

  return {}

def __LastActivityAddEquipmentCmd(client: StravaHttpClient, activity: Any) -> dict[str, str]:
  # If the activity is a type we have default gear for, then we set the gear.
  if activity["sport_type"] in EquipmentMap["sportTypes"]:
    gearId = EquipmentMap["gear"][EquipmentMap["sportTypes"][activity["sport_type"]]]
    return { "gear_id": gearId }

  return {}

def __SetupLogs() -> None:
  handler = logging.handlers.RotatingFileHandler('striver.log', maxBytes=100_000, backupCount=1)
  handler.setFormatter(logging.Formatter('{asctime} {levelname} {name} {filename}:{lineno} {message}', style='{'))
  logging.basicConfig(handlers=[handler], level=logging.getLevelName(LOG_LEVEL))

if __name__ == "__main__":
  main()