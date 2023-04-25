import random

import aiofiles
import aiohttp
import openai
import config
from config import *
import asyncio

async def create_text(text):
    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": text}
        ]
    )
    response = completion.choices[0].message['content']
    return response


async def create_image(text):
    response = await openai.Image.acreate(
        prompt=text,
        n=1,
        size="1024x1024"
    )
    img = response['data'][0]['url']
    async with aiohttp.ClientSession() as client_session:
        r = await client_session.get(img)
        n = random.randint(0, 1000000)
        path = fr'img{n}.jpg'
        async with aiofiles.open(path, 'wb') as file:
            await file.write(await r.read())
    return path


async def create_text_check_tokens():
    await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Привет"}
        ]
    )
