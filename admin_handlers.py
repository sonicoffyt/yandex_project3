import time
import types
from asyncio import sleep
from datetime import timedelta

import typing

import utils
from config import *
from db.__all_models import *
from pagination import *
from states import *
from db import db_session
from main_keyboards import *


@dp.message_handler(commands=['admin'], state='*')
@dp.callback_query_handler(lambda c: c.data == 'admin_panel', state='*')
async def admin_panel_view_admin_handler(message: typing.Union[types.Message, types.CallbackQuery], state: FSMContext):
    await state.finish()
    if message.from_user.id in ADMIN_IDS:
        if isinstance(message, types.CallbackQuery):
            await bot.edit_message_text('Вы в администраторской панели', message.from_user.id,
                                        message.message.message_id, reply_markup=admin_keyboard)
        else:
            await message.answer('Вы в администраторской панели', reply_markup=admin_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'count', state='*')
async def count(call: types.CallbackQuery):
    with db_session.create_session() as session:
        with session.begin():
            amount_users = session.query(User).count()
            await call.message.edit_text(f'Текущее кол-во пользователей: <code>{amount_users}</code>')


@dp.callback_query_handler(lambda c: c.data == 'mailing', state='*')
async def mailing(call: types.CallbackQuery):
    await bot.edit_message_text('Введите текст рассылки', call.from_user.id, call.message.message_id)
    await AdminPanel.mailing_wait.set()


@dp.message_handler(content_types=types.ContentType.ANY, state=AdminPanel.mailing_wait)
async def mailing(message: types.Message, state:FSMContext):
    with db_session.create_session() as session:
        with session.begin():
            users = session.query(User).all()
            for user in users:
                try:
                    await bot.copy_message(chat_id=user.user_id, from_chat_id=message.from_user.id,
                                           message_id=message.message_id)
                    await sleep(0.3)
                except (Exception,):
                    ...
            await message.answer('Рассылка успешно выполнена', reply_markup=return_to_main_admin_menu_kb)
            await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'ban', state='*')
async def ban_id(call: types.CallbackQuery):
    await AdminPanel.ban.set()
    await bot.edit_message_text('Введите айди пользователя, которого нужно забанить/разбанить', call.from_user.id,
                                call.message.message_id)


@dp.message_handler(state=AdminPanel.ban)
async def ban(message: types.Message):
    with db_session.create_session() as session:
        with session.begin():
            if not message.text.isalpha():
                user = session.query(User).where(User.user_id == int(message.text)).first()
                if user:
                    user.is_banned = not user.is_banned
                    await message.answer(
                        f'Пользователь {"забанен" if user.is_banned is True else "разбанен"}',
                        reply_markup=return_to_main_admin_menu_kb)
                else:
                    await message.answer('Пользователь не найден. Повторите попытку или отмените операцию',
                                         reply_markup=return_to_main_admin_menu_kb)
            else:
                await message.answer('Некорректный айди. Повторите попытку или отмените операцию',
                                     reply_markup=return_to_main_admin_menu_kb)


@dp.callback_query_handler(lambda c: c.data.startswith('next'), state='*')
async def next_(query: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        pagination = data['pagination']
        await pagination.on_next()
        if isinstance(pagination.text, list):
            await query.message.edit_text(pagination.text[pagination.current_page],
                                          reply_markup=await pagination.update_kb())
        else:
            await query.message.edit_text(pagination.text,
                                          reply_markup=await pagination.update_kb())


@dp.callback_query_handler(lambda c: c.data.startswith('previous'), state='*')
async def prev_(query: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        pagination = data['pagination']
        await pagination.on_prev()
        if isinstance(pagination.text, list):
            await query.message.edit_text(pagination.text[pagination.current_page - 2],
                                          reply_markup=await pagination.update_kb())
        else:
            await query.message.edit_text(pagination.text,
                                          reply_markup=await pagination.update_kb())
