from aiogram import types, F, Router, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# from bot.bot import USERS

router = Router()


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

    class photochooser(StatesGroup):
        photo_choosing = State()

        @router.message(StateFilter(None), F.text == "a")
        async def chooser(message: types.Message, state: FSMContext):
            await message.answer(
                text="Выберите фото"
            )
            await state.set_state(photo_choosing)

        @router.message(
            photochooser.photo_choosing,
            F.photo
        )
        async def photo(message: Message, state: FSMContext, bot: Bot):
            await bot.download(
                message.photo[-1],
                destination=f"/tmp/{message.photo[-1].file_id}.jpg"
            )


main()
