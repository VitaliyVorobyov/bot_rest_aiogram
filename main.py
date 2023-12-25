from aiogram import Bot, Dispatcher, F
import asyncpg
import asyncio
import logging
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator

from core.utils.settings import settings
from core.handlers.basic import get_photo
from core.utils.commands import set_commands
from core.handlers import basic, menu, discountcard, sendmessage, deleteusermessage, reserv
from core.middlewares.dbmiddleware import DbSession
from core.middlewares.apschadulermiddlewares import SchedulerMiddleware


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен!')


async def create_pool(host: str, port: int, username: str, password: str, database_name: str):
    return await asyncpg.create_pool(
        user=username, password=password, database=database_name, host=host, port=port
    )


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s -"
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

    storage: RedisStorage = RedisStorage.from_url(settings.redis.url)
    bot: Bot = Bot(token=settings.bots.bot_token)
    pool_connect: create_pool = await create_pool(
        host=settings.database.host,
        port=settings.database.port,
        username=settings.database.username,
        password=settings.database.password,
        database_name=settings.database.database_name)
    dp: Dispatcher = Dispatcher(storage=storage)
    jobstores = {
        'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                                 run_times_key='dispatched_trips_running', host=settings.redis.host, db=2,
                                 port=settings.redis.port)
    }
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone="Europe/Moscow", jobstores=jobstores))
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.start()

    dp.update.middleware.register(DbSession(pool_connect))
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.include_routers(basic.router, menu.router, discountcard.router,
                       sendmessage.router, reserv.router, deleteusermessage.router)
    dp.message.register(get_photo, F.photo)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as ex:
        logging.error(f"[!!! Exception] - {ex}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
