import asyncio
import json
import logging
import os

import aiohttp
import sqlalchemy.orm

from aiogram.utils import executor
from sqlalchemy import desc

import config
import utils
from admin_handlers import *
from ai import *
from check_api_token import check_api_tokens

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger.error("Starting bot")


@dp.message_handler(commands=['start'], state='*')
@dp.callback_query_handler(lambda c: c.data == 'return_to_main_menu', state='*')
async def cmd_start(message: typing.Union[types.Message, types.CallbackQuery], state: FSMContext):
    await state.finish()
    with db_session.create_session() as session:
        with session.begin():
            user = session.query(User).where(User.user_id == message.from_user.id).first()
            if message.from_user.id not in BANNED_USERS:
                if not user:
                    raw_user_id = message.text.split()[-1]
                    referer_first_level_id = 0
                    if raw_user_id.isdigit():
                        referer_first_level = session.query(User).where(User.user_id == int(raw_user_id)).first()
                        if referer_first_level:
                            referer_first_level_id = referer_first_level.user_id
                            await bot.send_message(chat_id=raw_user_id, text=f'У вас новый реферал, его username - '
                                                                             f'@{message.from_user.username}')
                    session.add(User(user_id=message.from_user.id, referer_first_level_id=referer_first_level_id,
                                     reset_tokens=(datetime.datetime.now() + timedelta(days=7)).strftime(
                                         '%d-%m-%Y %H:%M:%S')))
                    session.commit()
                else:
                    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    kb.row(types.KeyboardButton('🛡️Помощь'))
                    kb.row(types.KeyboardButton('👤Профиль'), types.KeyboardButton('🌄Создать картинку'))
                    kb.row(types.KeyboardButton('🔎Задать вопрос'))
                    if isinstance(message, types.CallbackQuery):
                        user.text = ''
                        user.last_answer = ''
                        user.last_question = ''
                        await message.message.delete()
                        await utils.send_img(message.from_user.id, PATH_START,
                                             '👋 Привет!\nТы попал в ChatGptBot.',
                                             kb)
                    else:
                        await utils.send_img(message.from_user.id, PATH_START,
                                             '👋 Привет!\nТы попал в ChatGptBot.',
                                             kb)




@dp.callback_query_handler(lambda c: c.data == 'help', state='*')
@dp.message_handler(lambda message: message.text == '🛡️Помощь', state='*')
@dp.message_handler(commands=['help'], state='*')
async def support(message: types.Message, state: FSMContext):
    if message.from_user.id not in BANNED_USERS:
        await state.finish()
        text = '''🦆Друзья, добро пожаловать на борт!

🤖Я - ChatGpt бот, готовый помочь вам во всем. Воспользуйтесь основными командами, чтобы получить необходимую информацию: /profile, /img, /ask.'''
        kb = types.InlineKeyboardMarkup()
        kb.row(types.InlineKeyboardButton('Картинки', callback_data='himg'))
        kb.row(types.InlineKeyboardButton('Поддержка', callback_data='hsup'),
               types.InlineKeyboardButton('ChatGPT - что это?', callback_data='hchatgpt'))
        if isinstance(message, types.CallbackQuery):
            await message.message.delete()
            await utils.send_img(message.from_user.id, PATH_HELP, text, kb)
        else:
            await utils.send_img(message.from_user.id, PATH_HELP, text, kb)


@dp.callback_query_handler(lambda c: c.data == 'hsup', state='*')
async def hsup(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    text = f"""
👨‍💻Я всегда готов помочь, если у вас возникнут вопросы, обращайтесь к - @slonic48. \n

"""
    if call.from_user.id not in BANNED_USERS:
        await call.message.delete()
        await utils.send_img(call.from_user.id, PATH_SUPPORT, text, return_to_help_menu_kb)




@dp.callback_query_handler(lambda c: c.data == 'hchatgpt', state='*')
async def hchatgpt(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    text = f"""
🤖 ChatGPT - это ИИ, способный общаться на любом языке и отвечать на вопросы. Он постоянно совершенствуется. ChatGPT доступен для всех, кто желает задать свой вопрос.

"""
    if call.from_user.id not in BANNED_USERS:
        await call.message.delete()
        await utils.send_img(call.from_user.id, PATH_GPT, text, return_to_help_menu_kb)


@dp.callback_query_handler(lambda c: c.data == 'himg', state='*')
async def himg(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    text = f"""
Для генерации картинки запрос нужно писать на английском языке.
"""
    if call.from_user.id not in BANNED_USERS:
        await call.message.delete()
        await utils.send_img(call.from_user.id, PATH_HIMG, text, return_to_help_menu_kb)


@dp.callback_query_handler(lambda c: c.data == 'profile', state='*')
@dp.message_handler(lambda message: message.text == '👤Профиль', state='*')
@dp.message_handler(commands=['profile'], state='*')
async def cabinet(message: types.Message, state: FSMContext):
    await state.finish()
    kb = types.InlineKeyboardMarkup()
    if message.from_user.id not in BANNED_USERS:
        with db_session.create_session() as session:
            with session.begin():
                user_id = message.from_user.id
                user = session.query(User).where(User.user_id == user_id).first()
                text = f'📊 Ваш профиль:\n' \
                       f'👤 ID: {user.user_id}\n'
            kb.row(types.InlineKeyboardButton('👨‍👩‍👧‍👦Реферальная система', callback_data='ref'))
            if isinstance(message, types.CallbackQuery):
                await message.message.delete()
                await utils.send_img(message.from_user.id, PATH_PROFILE, text, kb)
            else:
                await utils.send_img(message.from_user.id, PATH_PROFILE, text, kb)

@dp.callback_query_handler(lambda c: c.data == 'ref', state='*')
async def referrals(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    with db_session.create_session() as session:
        session: sqlalchemy.orm.Session
        with session.begin():
            amount_primary_referals = session.query(User).where(
                User.referer_first_level_id == call.from_user.id).count()
            text = f"""
📊 Реферальная система:

👥 Рефералов: {amount_primary_referals}

⚡️ Чтобы пригласить пользователя, дайте ему ссылку - https://t.me/{BOT_USERNAME}?start={call.from_user.id}
"""
            if call.from_user.id not in BANNED_USERS:
                await call.message.delete()
                await utils.send_img(call.from_user.id, PATH_REF, text, return_to_profile_menu_kb)

@dp.message_handler(lambda message: message.text == '🌄Создать картинку', state='*')
@dp.message_handler(commands=['img'], state='*')
async def ask(message: types.Message, state: FSMContext):
    if message.from_user.id not in BANNED_USERS:
        await state.finish()
        text = '🇺🇸 Введите запрос на английском языке'
        kb = types.InlineKeyboardMarkup()
        kb.row(types.InlineKeyboardButton('Отмена', callback_data="return_to_main_menu"))
        await message.answer(text, reply_markup=kb)
        await UserPanel.generate_img.set()


@dp.message_handler(state=UserPanel.generate_img, content_types=types.ContentTypes.ANY)
async def answer_question(message: types.Message, state: FSMContext):
    with db_session.create_session() as session:
        with session.begin():
            if message.from_user.id not in BANNED_USERS:
                user = session.query(User).where(User.user_id == message.from_user.id).first()
                if user.user_tariff_id == 3 or int(user.tokens_balance) >= 1000:
                    if int(user.time_to_new_request) >= 0:
                        await message.answer('🖼️ Рисую картинку')
                        await state.finish()
                        try:
                            user.time_to_new_request -= 10
                            path = await create_image(message.text)
                            await bot.send_photo(message.from_user.id, types.InputFile(path))
                            if user.user_tariff_id != 3:
                                user.tokens_balance -= 0
                            os.remove(path)
                            await state.finish()
                        except Exception as ex:
                            ...
                            await message.answer('Ошибка при генерации')
                            await state.finish()
                    else:
                        await message.answer(f'Вы недавно делали запрос. Ваша задержка по тарифу -'
                                             f' 10. '
                                             f'Осталось: {abs(user.time_to_new_request)} секунд')
                        await state.finish()
                else:
                    await message.answer('На балансе недостаточно токенов.')
                    await state.finish()


@dp.message_handler(lambda message: message.text == '🔎Задать вопрос', state='*')
@dp.message_handler(commands=['ask'], state='*')
@dp.callback_query_handler(lambda c: c.data == 'continue_dialog', state='*')
async def ask(message: types.Message, state: FSMContext):
    if message.from_user.id not in BANNED_USERS:
        await state.finish()
        with db_session.create_session() as session:
            with session.begin():
                if isinstance(message, types.CallbackQuery):
                    user = session.query(User).where(User.user_id == message.from_user.id).first()
                    kb = types.InlineKeyboardMarkup()
                    kb.row(types.InlineKeyboardButton('Отмена', callback_data="return_to_main_menu"))
                    text = f'Продолжайте диалог(1 токен = 1 символ)\n' \
                           f'Последний вопрос пользователя: {user.last_question[:20] + "..." if len(user.last_question) > 20 else user.last_question}\n' \
                           f'Последний ответ ИИ: {user.last_answer[:20] + "..." if len(user.last_answer) > 20 else user.last_answer}'
                    await message.message.edit_text(text, reply_markup=kb)
                    await UserPanel.ask_question.set()
                else:
                    kb = types.InlineKeyboardMarkup()
                    kb.row(types.InlineKeyboardButton('Отмена', callback_data="return_to_main_menu"))
                    text = '🔎 Задайте мне вопрос'
                    await message.answer(text, reply_markup=kb)
                    await UserPanel.ask_question.set()


@dp.message_handler(state=UserPanel.ask_question)
async def answer_question(message: types.Message, state: FSMContext):
    with db_session.create_session() as session:
        with session.begin():
            if message.from_user.id not in BANNED_USERS:
                user = session.query(User).where(User.user_id == message.from_user.id).first()
                text = f'Моё сообщение: {message.text}. Твоё сообщение: '
                len_text = len(text)
                if user.user_tariff_id == 3 or int(user.tokens_balance) >= len(message.text):
                    if user.time_to_new_request >= 0:
                        await message.answer('⏳ Вопрос принят, подготавливаю ответ')
                        user.time_to_new_request -= 10
                        await state.finish()
                        try:
                            user.text += text
                            answer = await create_text(user.text)
                            kb = types.InlineKeyboardMarkup()
                            kb.row(types.InlineKeyboardButton('Да', callback_data='continue_dialog'),
                                   types.InlineKeyboardButton('Нет', callback_data='return_to_main_menu'))
                            await message.answer(answer)
                            await message.answer('Продолжить диалог?', reply_markup=kb)
                            user.last_answer = answer
                            user.last_question = message.text
                            user.text += answer
                            if user.user_tariff_id != 3:
                                user.tokens_balance -= 0
                                user.tokens_balance -= 0
                            await state.finish()
                        except Exception as ex:
                            ...
                            user.text = user.text[:-len_text]
                            kb = types.InlineKeyboardMarkup()
                            kb.row(types.InlineKeyboardButton('Да', callback_data='continue_dialog'),
                                   types.InlineKeyboardButton('Нет', callback_data='return_to_main_menu'))
                            await message.answer(
                                'Ошибка при генерации. Повторить снова?(Вопрос нужно будет писать заново)',
                                reply_markup=kb)
                            await state.finish()
                        await state.finish()
                    else:
                        user.text = user.text[:-len_text]
                        kb = types.InlineKeyboardMarkup()
                        kb.row(types.InlineKeyboardButton('Да', callback_data='continue_dialog'),
                               types.InlineKeyboardButton('Нет', callback_data='return_to_main_menu'))
                        await message.answer(f'Вы недавно делали запрос.\n '
                                             f'Попробуйте снова через {abs(user.time_to_new_request)} секунд\n'
                                             f'Диалог сохранён до последнего ответа ИИ(нужно будет заново писать последний вопрос)\n'
                                             f'Повторить снова?',
                                             reply_markup=kb)
                        await state.finish()
                else:
                    await message.answer('На балансе недостаточно токенов.')
                    await state.finish()


async def time_to_new_message():
    while True:
        await asyncio.sleep(1)
        with db_session.create_session() as session:
            session: sqlalchemy.orm.Session
            with session.begin():
                users = session.query(User).where(User.time_to_new_request < 0).all()
                for user in users:
                    if user.is_banned is False:
                        try:
                            user.time_to_new_request += 1

                        except Exception as ex:
                            ...


async def banned_users():
    while True:
        await asyncio.sleep(60)
        with db_session.create_session() as session:
            with session.begin():
                users = session.query(User).all()
                try:
                    for user in users:
                        if user.is_banned is True:
                            config.BANNED_USERS.append(user.user_id)
                        else:
                            if user.user_id in config.BANNED_USERS:
                                config.BANNED_USERS.remove(user.user_id)
                except Exception as ex:
                    ...


if __name__ == "__main__":
    db_session.global_init("db/database.db")
    loop = asyncio.get_event_loop()
    loop.create_task(time_to_new_message())
    loop.create_task(banned_users())
    loop.create_task(check_api_tokens())
    executor.start_polling(dp, skip_updates=True)
