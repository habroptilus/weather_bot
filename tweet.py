from requests_oauthlib import OAuth1Session
import json
import settings
import random
import datetime

twitter = OAuth1Session(settings.CONSUMER_KEY,  settings.CONSUMER_SECRET,
                        settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

tweets = ["にゃーん", "わおーん"]

randomtweet = tweets[random.randrange(len(tweets))]
timestamp = datetime.datetime.today()
timestamp = str(timestamp.strftime("%Y/%m/%d %H:%M"))  # タイムスタンプを用意

params = {"status": randomtweet + " " + timestamp}
req = twitter.post(
    "https://api.twitter.com/1.1/statuses/update.json", params=params)
print(req)
