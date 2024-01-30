from aiogram import types, Router, Bot
from aiogram.filters import CommandStart

user_private_router = Router()

# snscrape --max-result 100 --since 2024-01-29 --jsonl telegram-channel slavuta_sity > telegram-@slavuta_sity.txt

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, bot: Bot):
    post = 'Перший пост'
    await bot.send_message(chat_id='@Slavuta_online', text=post)

