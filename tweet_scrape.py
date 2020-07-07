import os
import tweepy as tp
from dotenv import load_dotenv
from telegram import Bot
from botsql.db_utils import Users

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
        userid = 0
        results = []
        last_tweet = self.Users.get_lastweet(ac_id=1)
        chatid = -1001418848817
        try:
            for i in self.userslist:
                if last_tweet!=0:
                    twit=api.user_timeline(screen_name=i,count=20,max_id=last_tweet-1,include_retweets=True,tweet_mode = 'extended')
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
                self.Users.add_to_db(ac_id=userid,ac_name=i.screen_name,last_tweet=data['tweet_id'])
                userid=userid+1
                self.sendMessage(chat_id=chatid,text=str(data['text'])+"Via"+" ["+str(data['name'])+" ]",timeout=200)
    


    


