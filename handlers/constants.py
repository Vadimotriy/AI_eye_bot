from aiogram.fsm.state import StatesGroup, State


class PhotoChooser(StatesGroup):
    mode_choosing = State()
    photo_sending = State()


MODES = ['mode1', 'mode2']
BUTTONS = ['button1', 'button2']
