from aiogram import types, F, Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# from bot.bot import USERS
from handlers.constants import *

router = Router()


def main():
    # /start
    @router.message(F.text, Command('start'))
    async def start(message: types.Message):
        builder = ReplyKeyboardBuilder()
        for i in BUTTONS:
            builder.add(types.KeyboardButton(text=i))
        builder.adjust(2)

        text = 'asd'

        await message.answer(text=text, reply_markup=builder.as_markup(resize_keyboard=True))

    #button 1
    @router.message(StateFilter(None), F.text == "button1")
    async def chooser(message: types.Message, state: FSMContext):
        await message.answer(
            text=f"Выберите режим:"
        )
        await state.set_state(PhotoChooser.mode_choosing)

    @router.message(PhotoChooser.mode_choosing, F.text.lower().in_(MODES))
    async def chooser(message: types.Message, state: FSMContext):
        await state.update_data(chosen_mode=message.text.lower())
        await message.answer(
            text=f"Вы выбрали {message.text}. Отправьте фото:"
        )
        await state.set_state(PhotoChooser.photo_sending)

    # Ошибочный выбор
    @router.message(PhotoChooser.mode_choosing)
    async def chooser_incorrectly(message: types.Message):
        await message.answer(
            text="Я не знаю такого размера режима.\n\n"
                 f"Пожалуйста, выберите один из вариантов из списка ниже: {MODES}"
        )

    # Финал
    @router.message(PhotoChooser.photo_sending, F.photo)
    async def chooser(message: types.Message, state: FSMContext, bot: Bot):
        await bot.download(message.photo[-1], destination=f"../data/{message.photo[-1].file_id}.jpg")
        await message.answer(text=f"OK")
        await state.clear()

    # Ошибочный выбор
    @router.message(PhotoChooser.photo_sending)
    async def chooser_incorrectly(message: types.Message):
        await message.answer(
            text="Пришлите фото!"
        )

    # button2
    @router.message(StateFilter(None), F.text == "button2")
    async def chooser(message: types.Message, state: FSMContext):
        await message.answer(
            text=f"Отправьте фото:"
        )
        await state.set_state(NumberPhoto.photo_send)

    @router.message(NumberPhoto.photo_send, F.photo)
    async def chooser(message: types.Message, state: FSMContext, bot: Bot):
        await bot.download(message.photo[-1], destination=f"../data/{message.photo[-1].file_id}.jpg")
        await message.answer(text=f"OK")
        await state.clear()

    @router.message(PhotoChooser.photo_sending)
    async def chooser_incorrectly(message: types.Message):
        await message.answer(
            text="Пришлите фото!"
        )


main()
