from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery

from core.keyboards.inline import menu
from core.utils.callbackdata import MainMenu

router = Router()


@router.callback_query(MainMenu.filter(F.name_button == 'меню ресторана'))
async def select_menu(call: CallbackQuery, bot: Bot):
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=menu())
