from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from database.constants import *
# from bot.bot import USERS
from database.users_info import *
router_for_callbacks = Router()


def callbacks():
    @router_for_callbacks.callback_query(F.data.startswith('список'))
    async def send_random_value(callback: types.CallbackQuery):

        builder = InlineKeyboardBuilder()  # создание кнопки назад
        builder.add(types.InlineKeyboardButton(text=f"Назад", callback_data=f'back'))
        langs = '\n'.join(list(LANGUAGES_FOR_PHOTOES.keys()))
        await callback.message.edit_text(
            text=f"Вот список доступных языков:\n\n{langs}",
            reply_markup=builder.as_markup(),
        )
        await callback.answer()

    # функция кнопки назад. По большей части, нужно просто скопировать исходный хендлер
    @router_for_callbacks.callback_query(F.data.startswith('back'))
    async def send_random_value(callback: types.CallbackQuery):
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text=f"Список доступных языков",
            callback_data=f'список'))

        # единственное отличие это message.edit_text, а не message.answer
        sr = savedones(callback.from_user.id)
        await callback.message.edit_text(f'''Введите языки текстов (до трех включительно), которые есть на изображении {sr}\n''',
            reply_markup=builder.as_markup())
        await callback.answer()


callbacks()
