import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
# from data import MyDict
from AI.AI import AI

# логирование
logging.basicConfig(level=logging.INFO)

# USERS = MyDict()
AI = AI()

load_dotenv('data/.env')
API_TOKEN = os.getenv("API_TELEGRAM")
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
