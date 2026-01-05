from aiogram.dispatcher.filters.state import State, StatesGroup


class UserChannelInputting(StatesGroup):
    source_channel_url = State()
    target_channel_url = State()
    target_channel_apostol_id = State()


class DeleteChannelInputting(StatesGroup):
    channel_id = State()
