from aiogram import Dispatcher
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
import asyncio

from src.handlers.user.messages import Messages


def rate_limit(limit: float, key=None):
    """
    Decorator for configuring limits and keys for its functions.
    :param limit: seconds
    :param key: ключ
    :return: Callable
    """
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func
    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=0.8, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: Message, data: dict):
        """
        This handler is called when dispatcher receives a message

        :param message:
        """
        # Get the current handler
        handler = current_handler.get()
        # Get the dispatcher from the context
        dispatcher = Dispatcher.get_current()

        # If the handler was configured, we get the frequency limit and the handler key.
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            # Cancel handler execution
            raise CancelHandler()

    async def message_throttled(self, message: Message, throttled: Throttled):
        """
        Notify the user only when the limit is exceeded for the first time, and notify them of the unlock only when the limit is exceeded for the last time.
        :param message:
        :param throttled:
        """
        # Calculate how long you need to wait before the lock expires
        delta = throttled.rate - throttled.delta

        # Preventing flooding
        if throttled.exceeded_count <= 2:
            await message.reply(Messages.get_throttled_error())

        # We are waiting
        await asyncio.sleep(delta)

    async def on_process_callback_query(self, query: CallbackQuery, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()

        # If the handler was configured, we get the frequency limit and key
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.callback_query_throttled(query, t)
            # Cancel handler execution
            raise CancelHandler()

    async def callback_query_throttled(self, query: CallbackQuery, throttled: Throttled):
        delta = throttled.rate - throttled.delta

        if throttled.exceeded_count <= 2:
            await query.answer(Messages.get_throttled_error(), show_alert=True)

        await asyncio.sleep(delta)


def setup_middleware(dp):
    dp.middleware.setup(ThrottlingMiddleware())
