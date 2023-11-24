from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from datetime import datetime
import os

from core.utils.states import SendMessage
from core.keyboards.inline import main_menu
from core.utils.callbackdata import MainMenu
from core.keyboards.reply import contact, main_reply
from core.utils.googletable import AddMessage
from core.utils.deletemessage import delete_mess
from core.utils.dbconnect import Request


router = Router()


@router.callback_query(MainMenu.filter(F.name_button == 'напишите нам'))
async def select_message(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id,  text='Напишите ваше имя:',  reply_markup=main_reply())
    await state.set_state(SendMessage.name)


@router.message(SendMessage.name)
async def send_name(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(name=message.text.lower())
    await bot.send_message(chat_id=message.chat.id,
                           text=f'{message.text.capitalize()}, отправьте ваш номер телефона:',
                           reply_markup=contact())
    await state.set_state(SendMessage.number_phone)


@router.message(SendMessage.number_phone)
async def send_number(message: Message, bot: Bot, state: FSMContext):
    try:
        await state.update_data(number_phone=message.contact.phone_number)
    except AttributeError:
        await state.update_data(number_phone=message.text)
    context_data = await state.get_data()
    await bot.send_message(chat_id=message.chat.id,
                           text=f'{context_data.get("name").capitalize()}, напишите и отправите сообщение:',
                           reply_markup=main_reply())
    await state.set_state(SendMessage.text_states)


@router.message(SendMessage.text_states)
async def text(message: Message, bot: Bot, state: FSMContext, request: Request):
    context_data = await state.get_data()
    time_step = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    user_id = message.from_user.id
    name = context_data.get("name")
    number_phone = context_data.get("number_phone")
    message_text = message.text.lower()
    await AddMessage(time_step, user_id, name, number_phone, message_text).add_message()
    await request.add_massage(time_step, user_id, name, number_phone, message_text)
    await delete_mess(message, bot)
    photo = FSInputFile(os.path.abspath('media/startwindow/IMG_3432.JPG'))
    await bot.send_photo(chat_id=message.chat.id, photo=photo,
                         caption=f'Сообщение "{message.text}" отправлено', reply_markup=main_menu())
    await state.clear()
