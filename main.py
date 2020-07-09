import telegram
import logging
from telegram.ext import Updater,CommandHandler
import os
import tweet_scrape as ts
from dotenv import load_dotenv
import time

user_list = ["utdreport","manutd"]

def start(bot,update):
    Twitter_stream =  ts.TweetBot(user_list)
    Twitter_stream.fetch_tweets()
    print('Streaming to'+update.message.chat.title)

if __name__ == '__main__':
    user_list = ["utdreport","manutd"]
    load_dotenv("keys.env")
    API_TOKEN = str(os.getenv("TELEGRAM_BOT"))
    updater = Updater(token=API_TOKEN,use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start',start))
    updater.start_polling()
    updater.idle()

    
