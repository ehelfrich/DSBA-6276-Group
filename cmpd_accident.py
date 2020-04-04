import requests
import json
import pprint

response = requests.get('https://cmpdinfo.charlottenc.gov/api/v2/TrafficRSS')

print(response.content)
pprint.pprint(json.dumps(response.json()))
