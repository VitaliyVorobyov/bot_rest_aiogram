from aiogram import Bot
from core.keyboards.inline import confirm


async def send_message_time(bot: Bot, chat_id: int, date, name: str, time, guest_count, location):
    await bot.send_message(chat_id=chat_id, text=f'{name.capitalize()}, подтвердите резерв на {guest_count} персон '
                                                 f'{date} в {time} в ресторане по адресу {location}:',
                           reply_markup=confirm(date))
