from aiogram import types

from config import bot


async def send_img(user_id, path, text, kb=None):
    if kb:
        await bot.send_photo(user_id, photo=types.InputFile(path), caption=text, reply_markup=kb)
    else:
        await bot.send_photo(user_id, photo=types.InputFile(path), caption=text)
