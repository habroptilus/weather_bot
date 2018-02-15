import requests
import json


def setting():
    with open('api_key.txt', 'r') as f:
        apikey = list(f)[0].strip()
    return 'http://api.openweathermap.org/data/2.5/forecast?q={city},jp&units=metric&APPID=' + apikey


def getDatalist(city, today):
    url = api.format(city=city)
    r = requests.get(url)
    data = json.loads(r.text)
    if today:
        datalist = data["list"][:8]
    else:
        datalist = data["list"][8:16]
    return datalist


def getTempMaxAndMin(datalist):  # 単位は摂氏温度
    temp_max = []
    temp_min = []
    for data in datalist:
        temp_max.append(float(data["main"]["temp_max"]))
        temp_min.append(float(data["main"]["temp_min"]))
    return max(temp_max), min(temp_min)


def getWeather(datalist):
    morning = datalist[3]["weather"][0]["main"]
    evening = datalist[5]["weather"][0]["main"]
    night = datalist[7]["weather"][0]["main"]
    return morning, evening, night


def getMinPressure(datalist):  # 単位はhPa
    pressures = []
    for data in datalist:
        pressures.append(float(data["main"]["pressure"]))
    return min(pressures)


def debugPrint(datalist):
    for data in datalist:
        print(data["dt_txt"])


api = setting()
datalist = getDatalist("Tokyo", True)
debugPrint(datalist)
