import asyncio
import json
import subprocess

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import get_variable

from common.bot_cmds_list import private

token = get_variable('.env', 'TOKEN')

bot = Bot(token=token)
dp = Dispatcher()

ALLOWED_UPDATES = ['message', 'edited_message']


channels = ['slavuta_sity', ]


def collect_posts(channel):
    with open(f"{channel}.txt") as file:
        file = file.readlines()
    posts = []
    for n, line in enumerate(file):
        file[n] = json.loads(file[n])
        links = [link for link in file[n]['outlinks'] if channel not in link]
        p = str(file[n]['content']) + "\n\n" + str("\n".join(links))
        posts.append(p)
    return posts


def upload_posts(num_posts, channel):
    subprocess.run('chcp 65001', shell=True)
    command = f'snscrape --max-result {num_posts} --since 2024-01-29 --jsonl telegram-channel {channel} > {channel}.txt'
    subprocess.run(command, shell=True,  encoding='utf-8')


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


@dp.message()
async def get_channel(message: types.Message):
    try:
        channel, num_posts, target_channel = str(message.text).split()
        target_channel = "@" + target_channel

        upload_posts(num_posts, channel)
        posts = collect_posts(channel)
        while posts:
            await bot.send_message(target_channel, posts.pop())

        await bot.send_message(chat_id=message.from_user.id, text="Супер, копіювання постів завершено")

    except:
        await bot.send_message(chat_id=message.from_user.id, text="Неправильний формат. Натисни /post_from_telegram, щоб побачити правильний формат вводу")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())





















