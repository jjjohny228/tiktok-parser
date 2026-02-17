import asyncio

from aiogram import executor

from src.middlewares.throttling import setup_middleware
from src.handlers import register_all_handlers
from src.database.models import register_models
from src.create_bot import dp, bot
from src.utils import logger
from src.utils.scheduler import schedule_func, scheduler, async_schedule_func
from src.content_functions.parser import Parser
from src.handlers.user.user import Utils


async def on_startup(_):
    # Throttling registration
    setup_middleware(dp)

    # Handler registration
    register_all_handlers(dp)

    # Registering database models
    register_models()

    # Send database every day at 15pm
    schedule_func(Utils().send_database, trigger='cron', hour=15, minute=0)

    # Parse new videos every 15 minutes (one run at a time to avoid multiple Chrome instances)
    async_schedule_func(lambda: Parser().post_new_videos(), trigger='interval', minutes=15, misfire_grace_time=90, max_instances=1)

    scheduler.start()

    logger.info('The bot is up and running!')


async def on_shutdown(_):
    await (await bot.get_session()).close()


def start_bot():
    # try:
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
    # except Exception as e:
    #     logger.error(e)
