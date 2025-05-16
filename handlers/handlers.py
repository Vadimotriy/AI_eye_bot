from io import BytesIO
from PIL import Image

from aiogram import types, F, Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from bot.bot import AI
from database.constants import *
from handlers.queue import AsyncQueue
from database.users_info import *

router = Router()
quque = AsyncQueue()


def main():
    @router.message(F.text, Command('help'))
    async def start(message: types.Message):
        await message.answer(text="функции бота:\n\n <b> Nums Detector </b> принимает фото и выводит цифру, которая на нём изображена\n"
                                  "<b> распознать </b> объекты на фото - распознает и выводит объекты, \n"
                                  "которые, скорее всего, изображены на фото\n"
                                  "<b> распознать текст на фото </b> - принимает языки и выводит текст на этих языках с фото")
    # /start
    @router.message(F.text, Command('start'))
    async def start(message: types.Message):
        print(message.from_user.id)

        if message.from_user.id in ADMINS:
            buttons = BUTTONS[:] + ['⚙️АДМИН ПАНЕЛЬ⚙️']
        else:
            buttons = BUTTONS[:]

        builder = ReplyKeyboardBuilder()
        for i in buttons:
            builder.add(types.KeyboardButton(text=i))
        builder.adjust(1)

        text = 'Здравствуйте! выберите функцию, которая вам подходит. Что делают функции можете увидеть командой /help'

        await message.answer(text=text, reply_markup=builder.as_markup(resize_keyboard=True))

    # button 1
    @router.message(StateFilter(None), F.text == "распознать объекты на фото")
    async def chooser(message: types.Message, state: FSMContext):
        await message.answer(
            text=f"Отправьте фото:"
        )
        await state.set_state(PhotoChooser.photo_sending)

    @router.message(PhotoChooser.photo_sending, F.photo)
    async def chooser(message: types.Message, state: FSMContext, bot: Bot):
        await message.bot.send_chat_action(message.chat.id, 'typing')
        image = BytesIO()
        await bot.download(message.photo[-1], destination=image)
        try:
            result = AI.get_tags(image)
            print(result)

            await message.answer(result)

        except Exception as e:
            print(e)
            await message.answer("Извините! Произошла какая-то ошибка. Попробуйте повторить запрос позже.")

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
        sr = savedones(message.from_user.id)
        await message.answer(
            f'''Введите языки текстов (до трех включительно), которые есть на изображении {sr}\n''',
            reply_markup=builder.as_markup())
        await state.set_state(textphoto.langchoose)

    @router.message(textphoto.langchoose, F.text == "/skip")
    async def chooser(message: types.Message, state: FSMContext):
        txt = esh(message.from_user.id).split(' ')
        await state.update_data(langs=txt)
        await message.answer(f"Пришлите фото")
        await state.set_state(textphoto.photo_snd)

    @router.message(textphoto.langchoose, F.text)
    async def chooser(message: types.Message, state: FSMContext, bot: Bot):
        txt = message.text.split(' ')
        txt = txt if len(txt) <= 3 else txt[:3]
        flag = True
        for el in txt:
            if el.title() not in LANGUAGES_FOR_PHOTOES.keys():
                await message.answer(f"Такого языка нет в списке! - {el}")
                flag = False
        if flag:
            langs = ' '.join(txt)
            savedata(message.from_user.id, langs)
            await state.update_data(langs=txt)
            await message.answer(f"Пришлите фото")
            await state.set_state(textphoto.photo_snd)

    @router.message(textphoto.langchoose)
    async def chooser_incorrectly(message: types.Message):
        await message.answer(
            text="Введите языки текстов!"
        )

    @router.message(textphoto.photo_snd, F.photo)
    async def chooser(message: types.Message, state: FSMContext, bot: Bot):
        await message.bot.send_chat_action(message.chat.id, 'typing')
        image = BytesIO()
        await bot.download(message.photo[-1], destination=image)
        image = Image.open(image)

        langs = await state.get_data()
        langs = langs['langs']

        await quque.add_task(message.from_user.id, image, langs)
        await message.answer("Изображение добавлено в очередь. Мы пришлем результат как только будет готов!")

        await state.clear()

    # Ошибочный выбор
    @router.message(textphoto.photo_snd)
    async def chooser_incorrectly(message: types.Message):
        await message.answer(
            text="Пришлите фото!"
        )


main()
