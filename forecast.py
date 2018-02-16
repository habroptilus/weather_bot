import requests
import json
import math
city_ja = {"Tokyo": "東京"}


def setting():
    with open('api_key.txt', 'r') as f:
        apikey = list(f)[0].strip()
    return 'http://api.openweathermap.org/data/2.5/forecast?q={city},jp&units=metric&APPID=' + apikey


def getDatalist(api, city, today):
    url = api.format(city=city)
    r = requests.get(url)
    data = json.loads(r.text)
    if today:
        datalist = data["list"][:8]
    else:
        datalist = data["list"][4:12]
    return datalist


def getProperties(datalist):  # 単位は摂氏温度
    temp_max = []
    temp_min = []
    pressures = []
    speeds = []
    for data in datalist:
        temp_max.append(float(data["main"]["temp_max"]))
        temp_min.append(float(data["main"]["temp_min"]))
        pressures.append(float(data["main"]["pressure"]))
        speeds.append(float(data["wind"]["speed"]))
    p_max = max(pressures)
    p_min = min(pressures)
    pressure_diff = getMaxDiff(pressures)
    return round(max(temp_max), 1), round(min(temp_min), 1), max(speeds), pressure_diff


def getMaxDiff(pressures):  # 一番大きい気圧減少量を返す。単調増加してたら0を返す
    e_max = 0
    diff = 0
    for pressure in pressures:
        e_max = max(e_max, pressure)
        diff = max(e_max - pressure, diff)
    return diff


def getWeather(datalist):
    morning = datalist[3]["weather"][0]["main"]
    evening = datalist[5]["weather"][0]["main"]
    night = datalist[7]["weather"][0]["main"]
    return morning, evening, night


def debugPrint(datalist):
    for data in datalist:
        print(data["dt_txt"])


def generateTweet(city, today):
    api = setting()
    datalist = getDatalist(api, city, today)
    weather = getWeather(datalist)
    temp_max, temp_min, wind_max, pressure_diff = getProperties(datalist)
    greet, closing, day = getElement(today)
    if city in city_ja:
        tosimei = city_ja[city]
    else:
        tosimei = city
    if pressure_diff > 10:
        pressure = "気圧が大きく下がるから、頭痛持ちの人は気をつけてね。"
    else:
        pressure = ""
    if wind_max > 10:
        wind = "風が強くなりそうだから気をつけてね。"
    else:
        wind = ""

    tenki = getTenki(weather)
    tweet = "[{city}のお天気]\n{greet}\n{day}の{city}は{weather}"
    tweet += "気温は最高で{temp_max}°Cまで上がって、最低気温は{temp_min}°Cだって。{wind}{pressure}\n{closing}"
    print(pressure_diff)
    return tweet.format(greet=greet, day=day, city=tosimei, wind=wind, weather=tenki, pressure=pressure, temp_max=temp_max, temp_min=temp_min, closing=closing)


def getElement(today):
    if today:
        return "おはよー！", "今日もがんばってね。", "今日"
    else:
        return "今日もおつかれさま！", "ゆっくり休んでね。", "明日"


def getTenki(weather):
    if "Rain" in weather:
        if weather == ("Rain", "Rain", "Rain"):
            return "一日中ずっと雨みたい。やだね。"
        elif weather[0] == "Rain"and weather[1] == "Rain":
            return "夕方ぐらいまで雨だけど、夜にはやみそう。"
        elif weather[1] == "Rain" and weather[2] == "Rain":
            return "午後から雨が降りそう。昼からかも？"
        elif wether[0] == "Rain":
            return "朝は雨だけど、午後は雨が上がりそう。わーい。"
        elif weather[2] == "Rain":
            return "夜に雨が降り出しそう。傘持ってくといいかもね。"
        else:
            return "雨降るよ。あーめあがーりさしたまんまー傘がひとーつ。"
    elif "Snow" in weather:
        return "雪が降るよ！スノースマイル！"
    elif "Clear" not in weather and "Clouds" not in weather:
        return "よくわかんない！ごめんね。"
    elif weather == ("Clear", "Clear", "Clear"):
        return "とってもいい天気！"
    elif weather == ("Clouds", "Clouds", "Clouds"):
        return "一日中ずっとくもり。"
    else:
        return "晴れたり曇ったりするよ。ふつうが一番だね。"
