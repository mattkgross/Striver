import time
import requests
import json

# Define the endpoint for getting the user's latest activities
activities_endpoint = "https://www.strava.com/api/v3/athlete/activities"

# Define the endpoint for updating an activity
update_activity_endpoint = "https://www.strava.com/api/v3/activities/{}"

# Define a function to get the latest activities
def get_latest_activities():
    # Define query parameters for the API request
    params = {"per_page": 1}

    # Make the API request
    response = requests.get(activities_endpoint, headers=headers, params=params)

    # Check if the API request was successful
    if response.status_code == 200:
        # Parse the JSON response
        activities = json.loads(response.text)

        # Return the latest activity
        return activities[0] if activities else None
    else:
        # Print an error message if the API request failed
        print(f"Failed to get latest activities. Status code: {response.status_code}")
        return None

# Define a function to update an activity with hidden heart rate data
def update_activity(activity):
    # Check if the activity has heart rate data
    if "heartrate" in activity:
        # Hide the heart rate data
        activity["heartrate"] = None

        # Define the payload for the API request
        payload = {"activity": json.dumps(activity)}

        # Make the API request
        response = requests.put(update_activity_endpoint.format(activity["id"]), headers=headers, json=payload)

        # Check if the API request was successful
        if response.status_code == 200:
            print(f"Activity {activity['id']} updated successfully.")
        else:
            print(f"Failed to update activity {activity['id']}. Status code: {response.status_code}")
    else:
        print(f"Activity {activity['id']} has no heart rate data.")

# Run the program indefinitely
while True:
    # Get the latest activity
    latest_activity = get_latest_activities()

    # Check if there is a new activity
    if latest_activity:
        # Update the new activity with hidden heart rate data
        update_activity(latest_activity)

    # Wait for a minute before checking for new activities again
    time.sleep(60)

