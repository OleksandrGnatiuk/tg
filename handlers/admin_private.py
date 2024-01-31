import json
import subprocess
from aiogram import Bot, Router, types
from aiogram.filters import Command

from filters.chat_types import ChatTypeFilter


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]))

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


@admin_router.message()
async def get_channel(message: types.Message, bot: Bot):
    try:
        channel, num_posts, target_channel = str(message.text).split()
        target_channel = "@" + target_channel

        upload_posts(num_posts, channel)
        posts = collect_posts(channel)
        while posts:
            post = posts.pop()
            if post:
                await bot.send_message(target_channel, post)

        await bot.send_message(chat_id=message.from_user.id, text="Супер, копіювання постів завершено")

    except:
        await bot.send_message(chat_id=message.from_user.id, text="Неправильний формат. Натисни /post_from_telegram, щоб побачити правильний формат вводу")

