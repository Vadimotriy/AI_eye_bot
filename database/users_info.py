import logging

from aiogram import Bot, Dispatcher
from constants import API_TOKEN
from data import MyDict
from translator import My_Translator

# логирование
logging.basicConfig(level=logging.INFO)

USERS = MyDict()
Translator = My_Translator()
bot = Bot(token=API_TOKEN)
dp = Dispatcher()