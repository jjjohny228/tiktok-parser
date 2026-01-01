import os
from typing import Optional

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from src.database.user import get_user_targets
from src.filters.filter_func import check_is_admin
from src.utils import logger


class Keyboards:
    PAIRS_PER_PAGE = 4
    @staticmethod
    def get_signal_markup() -> InlineKeyboardMarkup:
        next_signal = InlineKeyboardButton('🔻 GET SIGNAL 🔻', callback_data='mines_next_signal')
        main_menu = InlineKeyboardButton('Choose another game 🔄', callback_data='client_menu')
        return InlineKeyboardMarkup(row_width=1).add(next_signal).add(main_menu)

    @staticmethod
    def get_menu_markup() -> InlineKeyboardMarkup:
        registration_button = InlineKeyboardButton('Registration📱', callback_data='mines_registration_menu')
        instruction_button = InlineKeyboardButton('Instruction📖', callback_data='mines_instruction_menu')
        get_signal_button = InlineKeyboardButton('🔻 GET SIGNAL 🔻', callback_data='mines_next_signal')
        return InlineKeyboardMarkup(row_width=2).add(registration_button, instruction_button).add(get_signal_button)

    @staticmethod
    def get_main_menu_markup(message: types.Message) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add('Подписка 🏧', 'Таргеты 🚀', 'Часто задаваемые вопросы ❔')
        if check_is_admin(message):
            keyboard.add('Меню админа')
        return keyboard

    @staticmethod
    def get_subscription_menu() -> ReplyKeyboardMarkup:
        active_subscription_button = KeyboardButton('Активная подписка')
        buy_subscription_button = KeyboardButton('Купить подписку')
        back_button = KeyboardButton('Назад в главное меню  ⬅️')
        return ReplyKeyboardMarkup(row_width=1).add(active_subscription_button, buy_subscription_button, back_button)

    @staticmethod
    def get_targets_menu() -> ReplyKeyboardMarkup:
        my_targets_button = KeyboardButton('Мои таргеты')
        add_target_button = KeyboardButton('Добавить таргет ➕')
        back_button = KeyboardButton('Назад в главное меню  ⬅️')
        return ReplyKeyboardMarkup(row_width=1).add(my_targets_button, add_target_button, back_button)

    @staticmethod
    def get_cancel_target_markup() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(row_width=1).add(KeyboardButton('Отменить добавление таргета'))

    @classmethod
    def get_my_targets_markup(cls, user_telegram_id: int, page: int = 0) -> Optional[InlineKeyboardMarkup]:
        user_targets = get_user_targets(user_telegram_id)
        keyboard = InlineKeyboardMarkup(row_width=2)
        start_idx = page * cls.PAIRS_PER_PAGE
        end_idx = start_idx + cls.PAIRS_PER_PAGE
        if not user_targets:
            logger.error("User doesnt have any targets")
            return
        current_targets = user_targets[start_idx:end_idx]

        # Add buttons with targets
        for target in current_targets:
            target_name = target.name
            target_id = target.id
            keyboard.insert(InlineKeyboardButton(text=target_name, callback_data=f"target_{target_id}"))

        # Pagination buttons
        total_pages = (len(user_targets) - 1) // cls.PAIRS_PER_PAGE + 1
        pagination_buttons = []

        if page > 0:
            pagination_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"page_{page - 1}_target"))

        pagination_buttons.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="none"))

        if end_idx < len(user_targets):
            pagination_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"page_{page + 1}_target"))

        keyboard.row(*pagination_buttons)

        # Back button
        keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data="my_targets_menu"))

        return keyboard

    @staticmethod
    def get_url_keyboard(url: str) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=1)
        url_button = InlineKeyboardButton(text='Обьявление🏠', url=url)
        keyboard.add(url_button)
        return keyboard

    # @classmethod
    # def get_signal_pairs_menu(cls, signal_type: str, page: int = 0) -> InlineKeyboardMarkup | None:
    #     keyboard = InlineKeyboardMarkup(row_width=2)
    #     start_idx = page * cls.PAIRS_PER_PAGE
    #     end_idx = start_idx + cls.PAIRS_PER_PAGE
    #     keyboard_pairs = cls.all_pairs.get(signal_type)
    #     if not keyboard_pairs:
    #         logger.error("There is no such pair type in all_pairs")
    #         return
    #     current_pairs = keyboard_pairs[start_idx:end_idx]
    #
    #     # Добавляем кнопки с валютными парами
    #     for pair in current_pairs:
    #         pair_text = pair[3:len(pair) - 3]
    #         keyboard.insert(InlineKeyboardButton(text=pair, callback_data=f"pair_{pair_text}"))
    #
    #     # Кнопки пагинации
    #     total_pages = (len(keyboard_pairs) - 1) // cls.PAIRS_PER_PAGE + 1
    #     pagination_buttons = []
    #
    #     if page > 0:
    #         pagination_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"page_{page - 1}_{signal_type}"))
    #
    #     pagination_buttons.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="none"))
    #
    #     if end_idx < len(keyboard_pairs):
    #         pagination_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"page_{page + 1}_{signal_type}"))
    #
    #     keyboard.row(*pagination_buttons)
    #
    #     # Кнопка "Назад"
    #     keyboard.add(InlineKeyboardButton(text="🔙Back", callback_data="start_callback"))
    #
    #     return keyboard





