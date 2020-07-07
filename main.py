import telegram
import logging
from telegram.ext import Updater
import os
from dotenv import load_dotenv

load_dotenv("keys.env")
API_TOKEN = str(os.getenv("TELEGRAM_BOT"))
updater = Updater(token='API_TOKEN',use_context=True)

