from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminPanel(StatesGroup):
    mailing_wait = State()
    ban = State()




class UserPanel(StatesGroup):
    ask_question = State()
    generate_img = State()


