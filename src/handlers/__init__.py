from aiogram import Dispatcher
from .user.user import register_user_handlers


def register_all_handlers(dp: Dispatcher):
    handlers = (
        register_user_handlers
    )
    for handler in handlers:
        handler(dp)
