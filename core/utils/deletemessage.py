from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message


async def delete_mess(message: Message, bot: Bot):
    count = 0
    while True:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - count)
            count += 1
        except TelegramBadRequest:
            break
