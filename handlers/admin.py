from aiogram import types, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.bot import AI
from database.constants import *
from database.functions import write, open_file

router_admin = Router()


def admin():
    # Вход в админ панель
    @router_admin.message(F.text == '⚙️АДМИН ПАНЕЛЬ⚙️')
    async def hello_admin(message: types.Message):
        if message.from_user.id in ADMINS:
            builder = ReplyKeyboardBuilder()
            for i in BUTTONS_ADMIN_BEFORE:
                builder.add(types.KeyboardButton(text=i))
            builder.adjust(1)

            await message.answer(
                text='Вы вошли в админ панель! Вы можете выбрать действие или вернуться обратно.',
                reply_markup=builder.as_markup(resize_keyboard=True)
            )
        else:
            await message.answer(text='Извините, у вас нет прав админа.')

    # Выход из админ панели
    @router_admin.message(F.text == 'Вернуться')
    async def bye_admin(message: types.Message):
        if message.from_user.id in ADMINS:
            buttons = BUTTONS[:] + ['⚙️АДМИН ПАНЕЛЬ⚙️']
            builder = ReplyKeyboardBuilder()
            for i in buttons:
                builder.add(types.KeyboardButton(text=i))
            builder.adjust(1)

            text = 'Вы вышли из админ панели.'

            await message.answer(text=text, reply_markup=builder.as_markup(resize_keyboard=True))
        else:
            await message.answer(text='Извините, у вас нет прав админа.')

    # Изменение точности для распознавания объектов по фото
    @router_admin.message(StateFilter(None), F.text == "Изменить точность")
    async def chooser(message: types.Message, state: FSMContext):
        if message.from_user.id in ADMINS:
            await message.answer(
                text=f"Отправьте точность (от 1 до 99):"
            )
            await state.set_state(AdminConf.conf_choose)
        else:
            await message.answer(text='Извините, у вас нет прав админа.')

    @router_admin.message(AdminConf.conf_choose, F.text)
    async def chooser(message: types.Message, state: FSMContext):
        if message.from_user.id in ADMINS:
            try:
                if 1 <= int(message.text) <= 99:
                    data = open_file()
                    write(data[0], int(message.text))
                    AI.update()
                    await message.answer(f"Новая точность - {int(message.text)}%.")
                    await state.clear()
                else:
                    raise ValueError
            except Exception as e:
                print(e)
                await message.answer(text='Точность должна быть целым числом от 1 до 99!')
        else:
            await message.answer(text='Извините, у вас нет прав админа.')

    # Ошибочный выбор
    @router_admin.message(AdminConf.conf_choose)
    async def chooser_incorrectly(message: types.Message):
        await message.answer(
            text="Отправьте точность (от 1 до 99)!"
        )

    # Выкл превод
    @router_admin.message(F.text == 'Отключить перевод')
    async def bye_admin(message: types.Message):
        if message.from_user.id in ADMINS:
            builder = ReplyKeyboardBuilder()
            for i in BUTTONS_ADMIN_AFTER:
                builder.add(types.KeyboardButton(text=i))
            builder.adjust(1)

            data = open_file()
            write(0, data[1])
            AI.update()


            await message.answer(text='Перевод отключен.', reply_markup=builder.as_markup(resize_keyboard=True))
        else:
            await message.answer(text='Извините, у вас нет прав админа.')

    # вкл перевода
    @router_admin.message(F.text == 'Включить перевод')
    async def bye_admin(message: types.Message):
        if message.from_user.id in ADMINS:
            builder = ReplyKeyboardBuilder()
            for i in BUTTONS_ADMIN_BEFORE:
                builder.add(types.KeyboardButton(text=i))
            builder.adjust(1)

            data = open_file()
            write(1, data[1])
            AI.update()

            await message.answer(text='Перевод включен.', reply_markup=builder.as_markup(resize_keyboard=True))
        else:
            await message.answer(text='Извините, у вас нет прав админа.')


admin()
