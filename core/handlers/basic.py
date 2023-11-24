from aiogram import Bot, Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import Command
import os
from aiogram.fsm.context import FSMContext
from core.utils.deletemessage import delete_mess

from core.keyboards.inline import main_menu
from core.utils.callbackdata import Back
from core.utils.dbconnect import Request
from core.utils.settings import settings


router = Router()


@router.message(Command("start"))
async def get_start(message: Message, bot: Bot, state: FSMContext, request: Request):
    await state.clear()
    await request.add_data(message.from_user.id, message.from_user.first_name)
    photo = FSInputFile(os.path.abspath('media/startwindow/IMG_3432.JPG'))
    await bot.send_photo(settings.bots.admin_id, photo, caption='Выберите опцию:',
                         reply_markup=main_menu())


@router.message(F.text == 'Главное меню')
async def main_menu_text(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await delete_mess(message, bot)
    photo = FSInputFile(os.path.abspath('media/startwindow/IMG_3432.JPG'))
    await bot.send_photo(settings.bots.admin_id, photo, caption='Выберите опцию:',
                         reply_markup=main_menu())


@router.callback_query(Back.filter(F.name_button == 'главное меню del'))
async def main_menu_text(call: CallbackQuery, bot: Bot):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    photo = FSInputFile(os.path.abspath('media/startwindow/IMG_3432.JPG'))
    await bot.send_photo(settings.bots.admin_id, photo, caption='Выберите опцию:',
                         reply_markup=main_menu())


@router.callback_query(Back.filter(F.name_button == 'главное меню'))
async def back_main_menu(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption='Выберите опцию:', reply_markup=main_menu())


async def get_photo(message: Message, bot: Bot):
    await message.answer(f'Изображение сохранено!')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'media/photo.jpg')
