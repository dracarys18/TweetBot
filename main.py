import telegram
import logging
from telegram.ext import Updater,CommandHandler
from urllib3.exceptions import ProtocolError
import os
import tweet_scrape as ts
from dotenv import load_dotenv
import time

load_dotenv("keys.env")
API_TOKEN = str(os.getenv("TELEGRAM_BOT"))

def startbot():
    Twitter_stream =  ts.TweetBot()
    Twitter_stream.fetch_tweets()

if __name__ == '__main__':
    updater = Updater(token=API_TOKEN,use_context=True)
    dispatcher = updater.dispatcher
    while True:
        try:
            startbot()
            time.sleep(5)
        except ProtocolError:
            continue
        