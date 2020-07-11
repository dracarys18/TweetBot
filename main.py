import telegram
import logging
from telegram.ext import Updater,CommandHandler
import os
import tweet_scrape as ts
from dotenv import load_dotenv
import time

user_list = ["utdreport","manutd","ManUnitedZone_"]

def startbot():
    Twitter_stream =  ts.TweetBot(user_list)
    Twitter_stream.fetch_tweets()

if __name__ == '__main__':
    load_dotenv("keys.env")
    API_TOKEN = str(os.getenv("TELEGRAM_BOT"))
    updater = Updater(token=API_TOKEN,use_context=True)
    dispatcher = updater.dispatcher
    while True:
        startbot()
        time.sleep(5)