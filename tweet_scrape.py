import os
import tweepy as tp
from dotenv import load_dotenv

load_dotenv("keys.env")
consumer_key = str(os.getenv("CONSUMER_KEY"))
consumer_secret = str(os.getenv("CONSUMER_SECRET"))
auth = tp.OAuthHandler(consumer_key,consumer_secret)
api = tp.API(auth)
users = ["utdreport","manutd"]
results =[]

try:
    for i in users:
        twit=api.user_timeline(screen_name=i,count=20,include_retweets=True,tweet_mode = 'extended')
        results.append(twit)
except tp.error.TweepError as err:
    print("K")

for k in results:
    for i in k:
        print(i.full_text+"\n")