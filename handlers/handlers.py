from io import BytesIO

from aiogram import types, F, Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot.bot import AI
from database.constants import *

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
        await message.answer(text=f"OK")
        await state.clear()

    # Ошибочный выбор
    @router.message(PhotoChooser.photo_sending)
    async def chooser_incorrectly(message: types.Message):
        await message.answer(
            text="Пришлите фото!"
        )

    # button2
    @router.message(StateFilter(None), F.text == "Nums Detector")
    async def chooser(message: types.Message, state: FSMContext):
        await message.answer(
            text=f"Отправьте фото:"
        )
        await state.set_state(NumberPhoto.photo_send)

    @router.message(NumberPhoto.photo_send, F.photo)
    async def chooser(message: types.Message, state: FSMContext, bot: Bot):
        image = BytesIO()
        await bot.download(message.photo[-1], destination=image)

        res = AI.predict_nums(image, False)
        text = ''
        for key, val in sorted(list(res.items()), key=lambda x: x[1]):
            text += f"{key} - {round(float(val * 100), 2)}%\n"
        await message.answer(text=text)
        await state.clear()

    @router.message(NumberPhoto.photo_send)
    async def chooser_incorrectly(message: types.Message):
        await message.answer(
            text="Пришлите фото!"
        )

    @router.message(StateFilter(None), F.text == "распознать текст на фото")
    async def chooser(message: types.Message, state: FSMContext):
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text=f"Список доступных языков",
            callback_data=f'список'))

        await message.answer(f'''введите языки текстов, которые есть на изображении или нажмите /skip\n''',
                             reply_markup=builder.as_markup())


    @router.message(NumberPhoto.photo_send, F.text)
    async def chooser(message: types.Message, state: FSMContext, bot: Bot):
        txt = message.text.split(' ')
        for el in txt:
            if el not in LANGUAGES_FOR_PHOTOES.keys():



def callbacks():
    @router_for_callbacks.callback_query(F.data.startswith('список'))
    async def send_random_value(callback: types.CallbackQuery):

        builder = InlineKeyboardBuilder()  # создание кнопки назад
        builder.add(types.InlineKeyboardButton(text=f"Назад", callback_data=f'back'))
        await callback.message.edit_text(
            text=f"{LANGUAGES_FOR_PHOTOES.keys()}",
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
        await callback.message.edit_text(f'''введите языки текстов, которые есть на изображении или нажмите /skip\n''',
                                        reply_markup=builder.as_markup())
        await callback.answer()


main()
callbacks()