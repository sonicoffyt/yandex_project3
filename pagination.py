from typing import Collection

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from config import dp


class Pagination:
    def __init__(self, buttons: Collection[InlineKeyboardButton], buttons_on_page: int = 5,
                 text: str or list = 'Выберите',
                 type_chat: str = 'return_to_main_menu') -> None:
        self._buttons = buttons
        self._buttons_on_page = buttons_on_page
        self.current_page = 0
        self.text = text
        self.type_chat = type_chat

    async def update_kb(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        from_ = self.current_page * self._buttons_on_page
        to_ = (self.current_page + 1) * self._buttons_on_page

        prev_button = InlineKeyboardButton("Назад",
                                           callback_data='previous')
        next_button = InlineKeyboardButton("Вперёд",
                                           callback_data='next')

        go_back = InlineKeyboardButton("В главное меню", callback_data=self.type_chat)

        for button in self._buttons[from_:to_]:
            markup.row(button)

        if from_ <= 0:
            return markup.row(next_button, go_back)
        elif to_ >= len(self._buttons):
            return markup.row(prev_button, go_back)
        return markup.row(prev_button, next_button, go_back)

    async def on_next(self) -> None:
        self.current_page += 1

    async def on_prev(self) -> None:
        self.current_page -= 1
