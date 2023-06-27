# This file contains all feature switches for the Strider application.

# Hides your latest activity's heart rate data (you can still see it).
RUN_LAST_ACTIVITY_HIDE_HR: bool = True
# If your latest activity has no description, fill it with a random quote.
RUN_LAST_ACTIVITY_ADD_QUOTE: bool = True
# If you specified equipment defaults for activity types, updates your last activity's data accordingly.
RUN_LAST_ACTIVITY_EQUIPMENT: bool = False # Strava just added this feature... finally.