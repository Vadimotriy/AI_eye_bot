import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from AI.AI import AI

# логирование
logging.basicConfig(level=logging.INFO)

load_dotenv('data/.env')
API_TOKEN = os.getenv("API_TELEGRAM")
IMAGGA_API = os.getenv("IMAGGA_API")
IMAGGA_SECRET_API = os.getenv("IMAGGA_SECRET_API")

AI = AI(IMAGGA_API, IMAGGA_SECRET_API)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
