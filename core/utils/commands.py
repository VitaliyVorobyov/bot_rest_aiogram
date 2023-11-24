from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='lang',
            description='Язык меню/Language'
        ),
        BotCommand(
            command='help',
            description='Пользовательское соглашение'
        ),
        BotCommand(
            command='offers',
            description='Сотрудничество и предложения'
        )

    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())