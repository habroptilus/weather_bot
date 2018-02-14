import requests
import json


with open('api_key.txt', 'r') as f:
    apikey = list(f)[0].strip()

api = "http://api.openweathermap.org/data/2.5/forecast/daily?id=1850147&units=metric&cnt=3&appid={key}"


url = api.format(key=apikey)
r = requests.get(url)
data = json.loads(r.text)

print("最低気温は{}度，最高気温は{}度".format(
    data["list"][0]["temp"]["min"], data["list"][0]["temp"]["max"]))
