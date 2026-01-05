from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton, ReplyKeyboardMarkup


class Keyboards:
    @staticmethod
    def get_menu_markup() -> ReplyKeyboardMarkup:
        channels_button = KeyboardButton('Channels')
        statistics_button = KeyboardButton('Statistics')
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(channels_button, statistics_button)

    @staticmethod
    def get_channels_markup(has_channels: bool) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
        add_channel_button = InlineKeyboardButton('Add channel ➕', callback_data='add_channel')
        delete_channel_button = InlineKeyboardButton('Delete channel 🗑', callback_data='delete_channel')
        if has_channels:
            keyboard.add(delete_channel_button)
        keyboard.add(add_channel_button)
        return keyboard

    @staticmethod
    def get_cancel_adding_channel_markup() -> ReplyKeyboardMarkup:
        cancel_adding_button = KeyboardButton('Cancel')
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(cancel_adding_button)






