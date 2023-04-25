import asyncio

import aiofiles

from ai import *
from config import *


async def check_api_tokens():
    fl = True
    while True:
        await asyncio.sleep(3)
        async with aiofiles.open(PATH_TO_AI_TOKENS, 'r+') as file:
            try:
                read = await file.readlines()
                if len(read) <= 1:
                    if fl:
                        fl = False
                        try:
                            for admin in ADMIN_IDS:
                                await bot.send_message(admin, 'Остался последний токен, либо их не осталось')
                                await asyncio.sleep(0.5)
                        except Exception as ex:
                            ...
                else:
                    fl = True
                for i in range(1):
                    token = read[i].strip()
                    openai.api_key = token
                    await create_text_check_tokens()
                    if openai.api_key != token:
                        openai.api_key = token
                else:
                    await asyncio.sleep(300)
            except Exception as ex:
                if str(ex) == "You exceeded your current quota, please check your plan and billing details."\
                        or str(ex)[:9] == 'Incorrect' or str(ex)[:49] == 'This key is associated with a deactivated account':
                    async with aiofiles.open(PATH_TO_INVALID_AI_TOKENS, 'a+') as f:
                        await f.write(token + '\n')
                    async with aiofiles.open(PATH_TO_AI_TOKENS, 'w') as inv_file:
                        del read[i]
                        await inv_file.writelines(read)

