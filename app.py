import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from common.bot_cmds_list import private
from handlers.admin_private import admin_router

bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)

dp = Dispatcher()
dp.include_router(admin_router)


ALLOWED_UPDATES = ['message', 'edited_message']


@dp.message(Command('post_from_telegram'))
async def post_cmd(message: types.Message):
    text = """
    Напиши:
    1. Назву каналу, звідки скопіювати пости
    2. скільки останніх постів перепостити
    3. назву каналу, в який необхідно запостити
    
    Приклад вводу:
    `slavuta_sity 10 Slavuta_online`
    """
    await message.reply(text=text)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())





















