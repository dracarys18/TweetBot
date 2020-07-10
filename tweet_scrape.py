import os
import time
import tweepy as tp
import telegram
import json
from dotenv import load_dotenv

load_dotenv("keys.env")
token = str(os.getenv("TELEGRAM_BOT"))
chatid = -1001422338305

class TwitterStream(tp.StreamListener):

    def on_data(self,data):
        try:
            d = json.loads(data)
            reply = d['in_reply_to_screen_name']
            tw_name = d['user']['name']
            if 'extended_tweet' in d:
                tg_text = d['extended_tweet']['full_text']
            else:
                tg_text = d['text']
            #print(reply)
            if(str(reply) == 'None'):
                if('RT @' not in tg_text):    
                    bot = telegram.Bot(token=token)
                    bot.sendMessage(chat_id=chatid,text=tg_text+"\n Via"+" ["+tw_name+" ]",timeout=200,disable_web_page_preview=False)
                    time.sleep(3)
                else:
                    print("It's a retweet so not posting it")
            else:
                print("It's a reply so not posting that")
        except Exception as e:
            print(e)

        return True

    def on_error(self, status_code):
        if status_code == 420:
            return False
        



class TweetBot():

    def __init__(self,user_list):
        self.userslist = list(user_list)

    def authorize(self):
        consumer_key = str(os.getenv("CONSUMER_KEY"))
        consumer_secret = str(os.getenv("CONSUMER_SECRET"))
        access_token = str(os.getenv("ACCESS_TOKEN"))
        access_token_secret = str(os.getenv("ACCESS_TOKEN_SECRET"))
        autho = tp.OAuthHandler(consumer_key,consumer_secret)
        autho.set_access_token(access_token,access_token_secret)
        return autho


    def fetch_tweets(self):
        api = self.authorize()
        listener = TwitterStream()
        account_list = self.get_tweet_acid(self.userslist)
        stream_tweet = tp.Stream(api,listener,tweet_mode='extended')
        stream_tweet.filter(follow=account_list,is_async=True)

    def get_tweet_acid(self,user_list):
        api = self.authorize()
        api_object = tp.API(api)
        list_id = []
        for i in user_list:
            user = api_object.get_user(screen_name=str(i))
            id = user.id
            list_id.append(str(id))
        return list_id        