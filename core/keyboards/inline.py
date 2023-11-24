from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackdata import (MainMenu, Back, Card, Rest,
                                     DateReserv, HourReserv, MinuteReserv,
                                     GuestReserv, Confirm, RestReserv)
from datetime import timedelta, datetime


def main_menu():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Новинки', web_app=WebAppInfo(url='https://teletype.in/@vitaliyvorobyev/PZMEsJ1SdcU'))
    keyboard_builder.button(text='Меню ресторана', callback_data=MainMenu(name_button='меню ресторана'))
    keyboard_builder.button(text='Карта гостя', callback_data=MainMenu(name_button='карта гостя'))
    keyboard_builder.button(text='Контакты', web_app=WebAppInfo(url='https://teletype.in/@vitaliyvorobyev/2ngQy-iHvA_'))
    keyboard_builder.button(text='Резервы', callback_data=MainMenu(name_button='резервы'))
    keyboard_builder.button(text='Напишите нам', callback_data=MainMenu(name_button='напишите нам'))
    keyboard_builder.adjust(2, 2, 2)
    return keyboard_builder.as_markup()


def menu():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Меню',
                            web_app=WebAppInfo(url='https://teletype.in/@vitaliyvorobyev/P96cJLyhK0K'))
    keyboard_builder.button(text='Бар',
                            web_app=WebAppInfo(url='https://teletype.in/@vitaliyvorobyev/P96cJLyhK0K'))
    keyboard_builder.button(text='Главное меню', callback_data=Back(name_button='главное меню'))
    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup()


def discount_card_create():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Условия', callback_data=Card(name_button='условия'))
    keyboard_builder.button(text='Завести карту', callback_data=Card(name_button='завести карту'))
    keyboard_builder.button(text='Перенос карты', callback_data=Card(name_button='перенос карты'))
    keyboard_builder.button(text='Главное меню', callback_data=Back(name_button='главное меню'))
    keyboard_builder.adjust(2, 1, 1)
    return keyboard_builder.as_markup()


def discount_card():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Инфо по карте', callback_data=Card(name_button='инфо по карте'))
    keyboard_builder.button(text='Предъявить', callback_data=Card(name_button='предъявить'))
    keyboard_builder.button(text='Главное меню', callback_data=Back(name_button='главное меню'))
    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup()


def discount_card_update():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Обновить код', callback_data=Card(name_button='обновить код'))
    keyboard_builder.button(text='Главное меню', callback_data=Back(name_button='главное меню del'))
    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup()


def reserv_list():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Мои резервы', callback_data=RestReserv(name_button='мои резервы'))
    keyboard_builder.button(text='Новый резерв', callback_data=RestReserv(name_button='новый резерв'))
    keyboard_builder.button(text='Главное меню', callback_data=Back(name_button='главное меню'))
    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup()


def new_reserv():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='ул. 1. д. 1', callback_data=Rest(
        name_button='ул. 1. д. 1'))
    keyboard_builder.button(text='ул. 2. д. 2', callback_data=Rest(
        name_button='ул. 2. д. 2'))
    keyboard_builder.button(text='Главное меню', callback_data=Back(name_button='главное меню'))
    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup()


def date_reserv(start_date):
    keyboard_builder = InlineKeyboardBuilder()
    start_date = datetime.strptime(start_date, "%d-%m-%Y")

    date_list = []
    if start_date.strftime("%d-%m-%Y") == datetime.now().strftime("%d-%m-%Y"):
        for day in range(0, 6):
            day = (start_date + timedelta(days=day)).strftime("%d-%m-%Y")
            date_list.append([day, 'date', day])
        date_list[0][0] = 'Сегодня'
        date_list[-1][0] = 'Далее>>'
        date_list[-1][1] = 'next'
    elif start_date.strftime("%d-%m-%Y") != datetime.now().strftime("%d-%m-%Y"):
        day = start_date.strftime("%d-%m-%Y")
        date_list.append([day, 'last', day])
        for day in range(0, 6):
            day = (start_date + timedelta(days=day)).strftime("%d-%m-%Y")
            date_list.append([day, 'date', day])
        date_list[0][0] = '<<Назад'
        date_list[-1][0] = 'Далее>>'
        date_list[-1][1] = 'next'
    for date in date_list:
        keyboard_builder.button(text=date[0], callback_data=DateReserv(add_name=date[1], name_button=date[2]))
    keyboard_builder.button(text='Гланое меню', callback_data=Back(name_button='главное меню'))
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def hour_reserv():
    keyboard_builder = InlineKeyboardBuilder()
    hour_list = [
        12, 13, 14, 15,
        16, 17, 18, 19,
        20, 21, 22
    ]
    for hour in hour_list:
        keyboard_builder.button(text=str(hour), callback_data=HourReserv(name_button=str(hour)))
    keyboard_builder.button(text='Гланое меню', callback_data=Back(name_button='главное меню'))
    keyboard_builder.adjust(3, 3, 3, 2, 1)
    return keyboard_builder.as_markup()


def minute_reserv():
    keyboard_builder = InlineKeyboardBuilder()
    minute_list = [
        '00', '15', '30', '45'
    ]
    for minute in minute_list:
        keyboard_builder.button(text=str(minute), callback_data=MinuteReserv(name_button=str(minute)))
    keyboard_builder.button(text='Гланое меню', callback_data=Back(name_button='главное меню'))
    keyboard_builder.adjust(4, 1)
    return keyboard_builder.as_markup()


def count_guest():
    keyboard_builder = InlineKeyboardBuilder()
    count_list = []
    for element in range(1, 21):
        count_list.append(element)
    for guest in count_list:
        keyboard_builder.button(text=str(guest), callback_data=GuestReserv(name_button=str(guest)))
    keyboard_builder.button(text='Гланое меню', callback_data=Back(name_button='главное меню'))
    keyboard_builder.adjust(5, 5, 5, 5, 1)
    return keyboard_builder.as_markup()


def back_inline():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Главное меню', callback_data=Back(name_button='главное меню'))
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def confirm(date):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Подтвердить', callback_data=Confirm(name_button='подтвержден', date=date))
    keyboard_builder.button(text='Отменить', callback_data=Confirm(name_button='отменен', date=date))
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()


def my_reserv_button(get):
    dates = [record['date'] for record in get]
    keyboard_builder = InlineKeyboardBuilder()
    for date in dates:
        if datetime.strptime(date, "%d-%m-%Y") > (datetime.now() - timedelta(days=1)):
            keyboard_builder.button(text=date, callback_data=DateReserv(add_name='мои резервы', name_button=date))
    keyboard_builder.button(text='Главное меню', callback_data=Back(name_button='главное меню'))
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()


def edit_my_reserv(date):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Перенести', callback_data=DateReserv(add_name=date, name_button='перенесен'))
    keyboard_builder.button(text='Отменить', callback_data=Confirm(name_button='отменен', date=date))
    keyboard_builder.button(text='Инфо', callback_data=DateReserv(add_name=date, name_button='инфо'))
    keyboard_builder.button(text='Главное меню', callback_data=Back(name_button='главное меню'))
    keyboard_builder.adjust(2, 1, 1)
    return keyboard_builder.as_markup()
