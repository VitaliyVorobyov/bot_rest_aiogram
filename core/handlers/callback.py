from aiogram import Bot
from aiogram.types import CallbackQuery
from core.keyboards.inline import new


async def select_main(call: CallbackQuery, bot: Bot):
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=new())
