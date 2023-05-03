import json
from client import StravaHttpClient

def main():
  stravaClient: StravaHttpClient = StravaHttpClient()
  print(json.dumps(stravaClient.GetLastActivity(), indent=2))

if __name__ == "__main__":
  main()