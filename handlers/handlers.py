from aiogram import types, F, Router
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
        buttons = []
        for i in buttons:
            builder.add(types.KeyboardButton(text=str(i)))
        builder.adjust(2)

        text = ''

        await message.answer(text=text, reply_markup=builder.as_markup(resize_keyboard=True))


main()
