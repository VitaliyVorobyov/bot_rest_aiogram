from aiogram import Bot, Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text)
async def delete(message: Message, bot: Bot):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
