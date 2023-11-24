from aiogram.fsm.state import State, StatesGroup


class SendMessage(StatesGroup):
    name = State()
    number_phone = State()
    text_states = State()


class Reserv(StatesGroup):
    select_rest = State()
    select_location = State()
    select_date = State()
    select_hour = State()
    select_minute = State()
    select_guest = State()
    send_name = State()
    send_number_phone = State()


class CreateCard(StatesGroup):
    name = State()
    number_phone = State()