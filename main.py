import telegram
import logging
from telegram.ext import Updater
import os
from dotenv import load_dotenv
from tweet_scrape import TweetBot
import time

if __name__ == '__main__':
    user_list = ["utdreport","manutd"]
    load_dotenv("keys.env")
    API_TOKEN = str(os.getenv("TELEGRAM_BOT"))
    updater = Updater(bot=TweetBot(user_list,API_TOKEN),use_context=True)
    dispatcher = updater.dispatcher
    yes = TweetBot(user_list,API_TOKEN)
    while True:
        yes.fetch_tweets()
        time.sleep(5)
    
