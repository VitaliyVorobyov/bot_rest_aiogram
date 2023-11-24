from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from datetime import datetime, timedelta
from aiogram.fsm.context import FSMContext
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.keyboards.inline import (date_reserv, hour_reserv, minute_reserv,
                                   main_menu, count_guest, new_reserv, reserv_list, my_reserv_button, edit_my_reserv)
from core.utils.callbackdata import (MainMenu, DateReserv, Rest, HourReserv, MinuteReserv, GuestReserv,
                                     RestReserv, Confirm)
from core.utils.states import Reserv
from core.keyboards.reply import main_reply, contact
from core.utils.deletemessage import delete_mess
from core.utils.googletable import AddMessage
from core.utils.dbconnect import Request
from core.handlers.apsched import send_message_time


router = Router()


@router.callback_query(MainMenu.filter(F.name_button == 'резервы'))
async def reserv(call: CallbackQuery, bot: Bot):
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=reserv_list())


@router.callback_query(RestReserv.filter(F.name_button == 'мои резервы'))
async def my_reserv(call: CallbackQuery, bot: Bot, request: Request):
    get = await request.reserv_edit(call.from_user.id)
    if len([el for el in list(map(lambda date: datetime.strptime(date, "%d-%m-%Y"),
                                  [record['date'] for record in get])) if el >= datetime.now()]) == 0:
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='У вас нет активных резервов', reply_markup=reserv_list())
    else:
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption=f'Выберите резерв, для просмотра информации о нем',
                                       reply_markup=my_reserv_button(get))


@router.callback_query(DateReserv.filter(F.add_name == 'мои резервы'))
async def edit_reserv(call: CallbackQuery, bot: Bot, callback_data: DateReserv):
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption=f'Вы выбрали {callback_data.name_button}',
                                   reply_markup=edit_my_reserv(callback_data.name_button))


@router.callback_query(DateReserv.filter(F.name_button == 'перенесен'))
async def transport(call: CallbackQuery, bot: Bot, callback_data: DateReserv, request: Request):
    await request.confirm_reserv(user_id=call.from_user.id, date=callback_data.add_name,
                                 conf=callback_data.name_button)
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption=f'ВНИМАНИЕ!!!\nПри переносе текущий резерв отменяется!',
                                   reply_markup=new_reserv())


@router.callback_query(DateReserv.filter(F.name_button == 'инфо'))
async def info_reserv(call: CallbackQuery, bot: Bot, callback_data: DateReserv, request: Request):
    get = await request.reserv_info(call.from_user.id, callback_data.add_name)
    dates = [record['date'] for record in get][0]
    time = [record['time'] for record in get][0]
    location = [record['location'] for record in get][0]
    guest_count = [record['guest_count'] for record in get][0]
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption=f'Информация по резерву:\n\nРесторан по адресу: {location}\n'
                                           f'Дата: {dates}\nВремя: {time}\nКоличество гостей: {guest_count}',
                                   reply_markup=reserv_list())


@router.callback_query(RestReserv.filter(F.name_button == 'новый резерв'))
async def select_rest(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption='Выберите ресторан:', reply_markup=new_reserv())
    await state.set_state(Reserv.select_location)


@router.callback_query(Rest.filter(), Reserv.select_location)
async def select_date(call: CallbackQuery, bot: Bot, callback_data: Rest, state: FSMContext):
    date = datetime.now().strftime("%d-%m-%Y")
    await state.update_data(select_location=callback_data.name_button)
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption='Выберите дату резерва:', reply_markup=date_reserv(date))
    await state.set_state(Reserv.select_date)


@router.callback_query(Reserv.select_date, DateReserv.filter(F.add_name == 'date'))
async def select_hour(call: CallbackQuery, bot: Bot, callback_data: DateReserv, state: FSMContext):
    date = callback_data.name_button
    await state.update_data(select_date=date)
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption='Выберите час резерва:', reply_markup=hour_reserv())
    await state.set_state(Reserv.select_hour)


@router.callback_query(Reserv.select_hour, HourReserv.filter())
async def select_minutes(call: CallbackQuery, bot: Bot, callback_data: DateReserv, state: FSMContext):
    hour = callback_data.name_button
    await state.update_data(select_hour=hour)
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption='Выберите интервал:', reply_markup=minute_reserv())
    await state.set_state(Reserv.select_minute)


@router.callback_query(Reserv.select_minute, MinuteReserv.filter())
async def select_guest_count(call: CallbackQuery, bot: Bot, callback_data: DateReserv, state: FSMContext):
    minute = callback_data.name_button
    await state.update_data(select_minute=minute)
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption='Выберите количество гостей:', reply_markup=count_guest())
    await state.set_state(Reserv.select_guest)


@router.callback_query(Reserv.select_guest, GuestReserv.filter())
async def send_name(call: CallbackQuery, bot: Bot, callback_data: DateReserv, state: FSMContext):
    count = callback_data.name_button
    await state.update_data(select_guest=count)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id,  text='Напишите ваше имя:',  reply_markup=main_reply())
    await state.set_state(Reserv.send_name)


@router.message(Reserv.send_name)
async def send_number(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(send_name=message.text.lower())
    await bot.send_message(chat_id=message.chat.id,
                           text=f'{message.text.capitalize()}, отправьте ваш номер телефона:',
                           reply_markup=contact())
    await state.set_state(Reserv.send_number_phone)


@router.message(Reserv.send_number_phone)
async def save_reserv(message: Message, bot: Bot, state: FSMContext, request: Request, apscheduler: AsyncIOScheduler):
    try:
        await state.update_data(send_number_phone=message.contact.phone_number)
    except AttributeError:
        await state.update_data(send_number_phone=message.text)
    context_data = await state.get_data()
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    user_id = message.from_user.id
    name = context_data.get("send_name")
    number_phone = context_data.get("send_number_phone")
    location = context_data.get("select_location")
    date = context_data.get("select_date")
    time = f'{context_data.get("select_hour")}:{context_data.get("select_minute")}'
    guest_count = context_data.get("select_guest")
    await AddMessage(timestamp, user_id, name, number_phone, location, date, time, guest_count).add_reserv()
    await request.add_reserv(timestamp, user_id, name, number_phone, location, date, time, guest_count)
    await delete_mess(message, bot)
    photo = FSInputFile(os.path.abspath('media/startwindow/IMG_3432.JPG'))
    await bot.send_photo(chat_id=message.chat.id, photo=photo,
                         caption=f'{name.capitalize()}, резерв на {guest_count} персон '
                                 f'{date} в {time} в ресторане по адресу {location} принят!',
                         reply_markup=main_menu())
    await state.clear()
    triger_date = datetime.strptime(date, '%d-%m-%Y') - timedelta(days=1) + timedelta(
        hours=int(time.split(":")[0]), minutes=int(time.split(":")[1]))
    apscheduler.add_job(send_message_time, trigger='date', run_date=datetime.now()+timedelta(seconds=10),
                        kwargs={'chat_id': user_id, 'name': name, 'date': date,
                                'time': time, 'location': location, 'guest_count': guest_count})


@router.callback_query(DateReserv.filter(F.add_name == 'next'))
async def update_date(call: CallbackQuery, bot: Bot, callback_data: DateReserv):
    date = callback_data.name_button
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=date_reserv(date))


@router.callback_query(DateReserv.filter(F.add_name == 'last'))
async def update_date(call: CallbackQuery, bot: Bot, callback_data: DateReserv):
    date = callback_data.name_button
    next_date = (datetime.strptime(date, "%d-%m-%Y") - timedelta(days=5)).strftime("%d-%m-%Y")
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=date_reserv(next_date))


@router.callback_query(Confirm.filter())
async def true_confirm(call: CallbackQuery, bot: Bot, callback_data: Confirm, request: Request):
    await request.confirm_reserv(user_id=call.from_user.id, date=callback_data.date,
                                 conf=callback_data.name_button)
    await delete_mess(call.message, bot)
    photo = FSInputFile(os.path.abspath('media/startwindow/IMG_3432.JPG'))
    await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=f'Резерв {callback_data.name_button}!',
                         reply_markup=main_menu())
