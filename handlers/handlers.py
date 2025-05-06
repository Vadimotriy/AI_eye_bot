from aiogram import types, F, Router, Dispatcher
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# from bot.bot import USERS

router = Router()
router_for_translate = Router()

def main():
    # /start
    @router.message(F.text, Command('start'))
    async def start(message: types.Message):
        builder = ReplyKeyboardBuilder()
        buttons = ['a', 'b']
        for i in buttons:
            builder.add(types.KeyboardButton(text=str(i)))
        builder.adjust(2)

        text = 'asd'

        await message.answer(text=text, reply_markup=builder.as_markup(resize_keyboard=True))

    @router.message(F.text, Command('help'))
    async def help(message: types.Message):
        await message.reply(f'Для использования бота, пожалуйста, выберите одну из кнопок которые вам нужны.')

main()
