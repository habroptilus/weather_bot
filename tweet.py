from requests_oauthlib import OAuth1Session
import json
import settings
import random
import forecast

twitter = OAuth1Session(settings.CONSUMER_KEY,  settings.CONSUMER_SECRET,
                        settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
tweet = forecast.generateTweet("Tokyo", today=False)
params = {"status": tweet}

req = twitter.post(
    "https://api.twitter.com/1.1/statuses/update.json", params=params)
if req.status_code == 200:
    print("Success!")
else:
    print("Error!")
