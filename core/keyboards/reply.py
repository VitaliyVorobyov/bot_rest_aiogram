from aiogram.utils.keyboard import ReplyKeyboardBuilder


def contact():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text='Отправить номер телефона', request_contact=True)
    keyboard_builder.button(text='Главное меню')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True,
                                      input_field_placeholder='Перейди в главное меню')


def main_reply():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text='Главное меню')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True,
                                      input_field_placeholder='Перейди в главное меню')