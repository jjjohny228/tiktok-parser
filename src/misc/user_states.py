from aiogram.dispatcher.filters.state import State, StatesGroup


class UserTargetInputting(StatesGroup):
    target_name = State()
    target_url = State()
    target_chat_id = State()

