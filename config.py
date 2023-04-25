from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


TOKEN = ''
PATH_TO_AI_TOKENS = r'ai_tokens.txt'
PATH_TO_INVALID_AI_TOKENS = r'invalid_ai_tokens.txt'
ADMIN_IDS = ()
BOT_USERNAME = ''
BANNED_USERS = []
bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

PATH_START = r'menu.png'
PATH_HELP = r'menu.png'
PATH_PROFILE = r'profile.png'


PATH_HIMG = r'HIMG.png'
PATH_GPT = r'GPT.png'
PATH_SUPPORT = r'SUPPORT.png'
PATH_REF = r'REF.png'
