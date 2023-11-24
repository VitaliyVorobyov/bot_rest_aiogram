from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from datetime import datetime
import os
from aiogram.exceptions import TelegramBadRequest

from core.keyboards.inline import discount_card_create, main_menu, discount_card, discount_card_update
from core.keyboards.reply import contact, main_reply
from core.utils.callbackdata import MainMenu, Card
from core.utils.states import CreateCard
from core.utils.deletemessage import delete_mess
from core.utils.dbconnect import Request
from core.utils.qr_generate import generate_qr_code


router = Router()


@router.callback_query(MainMenu.filter(F.name_button == 'карта гостя'))
async def select_card(call: CallbackQuery, bot: Bot, request: Request):
    get = await request.card_info(call.from_user.id)
    if get is None:
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=discount_card_create())
    else:
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=discount_card())


@router.callback_query(Card.filter(F.name_button == 'завести карту'))
async def create_card(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id, text='Напишите ваше имя:', reply_markup=main_reply())
    await state.set_state(CreateCard.name)


@router.message(CreateCard.name)
async def send_name(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(name=message.text.lower())
    await bot.send_message(chat_id=message.chat.id,
                           text=f'{message.text.capitalize()}, отправьте ваш номер телефона:',
                           reply_markup=contact())
    await state.set_state(CreateCard.number_phone)


@router.message(CreateCard.number_phone)
async def send_name(message: Message, bot: Bot, state: FSMContext, request: Request):
    try:
        await state.update_data(number_phone=message.contact.phone_number)
    except AttributeError:
        await state.update_data(number_phone=message.text)
    context_data = await state.get_data()
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    user_id = message.from_user.id
    name = context_data.get("name")
    number_phone = context_data.get("number_phone")
    await request.create_card(user_id, timestamp, name, number_phone)
    await delete_mess(message, bot)
    photo = FSInputFile(os.path.abspath('mmedia/startwindow/IMG_3432.JPG'))
    await bot.send_photo(chat_id=message.chat.id, photo=photo,
                         caption=f'{name.capitalize()}, ваша карта создана.\nСкидка по карте 10%',
                         reply_markup=main_menu())
    await state.clear()


@router.callback_query(Card.filter(F.name_button == 'инфо по карте'))
async def create_card(call: CallbackQuery, bot: Bot, request: Request):
    try:
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption=f'Ваша скидка: {await request.card_info(call.from_user.id)}%',
                                       reply_markup=discount_card())
    except TelegramBadRequest:
        pass


@router.callback_query(Card.filter(F.name_button == 'условия'))
async def create_card(call: CallbackQuery, bot: Bot):
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption=f'Условия карты гостя:\n -Первоначальная скидка 10%.',
                                   reply_markup=discount_card_create())


@router.callback_query(Card.filter(F.name_button == 'перенос карты'))
async def create_card(call: CallbackQuery, bot: Bot):
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption=f'Функция в разработке',
                                   reply_markup=discount_card_create())


@router.callback_query(Card.filter(F.name_button == 'предъявить'))
async def create_card(call: CallbackQuery, bot: Bot):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await generate_qr_code(call.from_user.id)
    photo = FSInputFile(f'media/{call.from_user.id}.jpg')
    await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption='Предъявите код',
                         reply_markup=discount_card_update())
    os.remove(f'media/{call.from_user.id}.jpg')


@router.callback_query(Card.filter(F.name_button == 'обновить код'))
async def create_card(call: CallbackQuery, bot: Bot):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await generate_qr_code(call.from_user.id)
    photo = FSInputFile(f'media/{call.from_user.id}.jpg')
    await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption='Предъявите код',
                         reply_markup=discount_card_update())
    os.remove(f'media/{call.from_user.id}.jpg')
