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
        n = self.set_last_tweet(userid)
        chatid = -1001422338305
        try:
            for i in self.userslist:
                if n!=0:
                    twit=api.user_timeline(screen_name=i,count=20,since_id=n,include_retweets=True,tweet_mode = 'extended')
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
                try:
                    db.add_to_db(ac_id=str(userid),ac_name=str(data['name']),last_tweet=int(data['tweet_id']))
                except:
                    db.update_lastweet(ac_id=str(userid),last_tweet=int(data['tweet_id']))
                userid=userid+1
                n = self.set_last_tweet(userid)
                self.sendMessage(chat_id=chatid,text=str(data['text'])+"\n Via"+" ["+str(data['name'])+" ]",timeout=200,disable_web_page_preview=False)
                time.sleep(5)
    
    def set_last_tweet(self,user_id):
        db = Users()
        last_tweet = db.get_lastweet(ac_id=int(user_id))
        try:
            k = int(last_tweet[0][0])
        except:
            k=0
        return k





    


