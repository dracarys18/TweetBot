import os
import time
import tweepy as tp
from dotenv import load_dotenv
from telegram import Bot
from db_utils import Users

class TweetBot(Bot):

    def __init__(self,user_list,token):
        super().__init__(token=token)
        self.userslist = list(user_list)

    def fetch_tweets(self):
        load_dotenv("keys.env")
        consumer_key = str(os.getenv("CONSUMER_KEY"))
        consumer_secret = str(os.getenv("CONSUMER_SECRET"))
        auth = tp.OAuthHandler(consumer_key,consumer_secret)
        api = tp.API(auth)
        db = Users()
        userid = 0
        results = []
        last_tweet = db.get_lastweet(ac_id=1)
        try:
            k = int(last_tweet[0][0])
        except:
            k=0
        chatid = -1001418848817
        try:
            for i in self.userslist:
                if k!=0:
                    twit=api.user_timeline(screen_name=i,count=20,max_id=k-1,include_retweets=True,tweet_mode = 'extended')
                    results.append(twit)
                else:
                    twit = api.user_timeline(screen_name=i,count=20,include_retweets=True,tweet_mode = 'extended')
                    results.append(twit)
        except tp.error.TweepError as err:
            print(str(err))
        for k in results:
            for i in k:
                data = {
                    'tweet_id'  : i.id ,
                    'name'  : i.user.name,             
                    'text'  : i.full_text
                }
                db.add_to_db(ac_id=str(userid),ac_name=str(data['name']),last_tweet=int(data['tweet_id']))
                userid=userid+1
                self.sendMessage(chat_id=chatid,text=str(data['text'])+"Via"+" ["+str(data['name'])+" ]",timeout=200)
                time.sleep(5)
    


    


