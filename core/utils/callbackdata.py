from aiogram.filters.callback_data import CallbackData


class MainMenu(CallbackData, prefix='main'):
    name_button: str


class Back(CallbackData, prefix='back'):
    name_button: str


class Card(CallbackData, prefix='card'):
    name_button: str


class SendMessage(CallbackData, prefix='send message'):
    name_button: str


class RestReserv(CallbackData, prefix='rest_reserv'):
    name_button: str


class Rest(CallbackData, prefix='rest'):
    name_button: str


class DateReserv(CallbackData, prefix='date reserv'):
    add_name: str
    name_button: str


class HourReserv(CallbackData, prefix='hour'):
    name_button: str


class MinuteReserv(CallbackData, prefix='minute'):
    name_button: str


class GuestReserv(CallbackData, prefix='minute'):
    name_button: str


class Confirm(CallbackData, prefix='confirm'):
    name_button: str
    date: str
