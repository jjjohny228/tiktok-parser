import os
import datetime
import random

from aiogram.types import InputFile

from config import Config


class Messages:
    @staticmethod
    def get_loading() -> str:
        return '♻ Loading...'

    @staticmethod
    def get_welcome() -> str:
        return 'Добро пожаловать в бота. '

    @staticmethod
    def get_menu_photo() -> str:
        return 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fcommons.wikimedia.org%2Fwiki%2FFile%3ATest-Logo.svg&psig=AOvVaw0lG3HvYAtKg_y2_IAqDwOr&ust=1763831042425000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCIDh4-jcg5EDFQAAAAAdAAAAABAE'

    @staticmethod
    def get_instruction_text() -> str:
        return (
            "The bot is based on and trained using OpenAI's neural network cluster 🖥[ChatGPT-v4].\n\n"
            "For training, the bot played 🎰over 8000 games.\nCurrently, bot users successfully make 20-30% of their 💸 capital daily!\n\n"
            "The bot is still learning, and its accuracy is at 87%!\n\n "
            "Follow these instructions for maximum profit: \n\n"
            "🔸 1.  Register at the 1WIN. If it doesn’t open - use a VPN (Sweden). I use VPN Super Unlimited Proxy\n\n"
            "🔸 2. Deposit funds into your account.\n\n"
            "🔸 3. Go to the 1win games section and select the 💣'MINES' game.\n\n"
            "🔸 4. Set the number of traps to three. This is important!\n\n"
            "🔸 5. Request a signal from the bot and place bets based on the bot’s signals.\n\n"
            "🔸 6. In case of a losing signal, we advise you to double (X2) your bet to fully cover the loss in the next signal."
        )

    @staticmethod
    def get_instruction_video() -> InputFile:
        return InputFile('resources/mines/instruction.mp4')

    @staticmethod
    def get_throttled_error() -> str:
        return 'Пожалуйста, не так часто 🙏'

    @staticmethod
    def get_add_taget_name_text():
        return 'Введите название таргета:'

    @staticmethod
    def get_add_taget_url_text():
        return 'Введите url таргета  (ссылка должна быть со всеми нужными фильтрами):'

    @staticmethod
    def get_add_taget_chat_id_text():
        return ('Введите id чата куда будут присылаться результаты (обязательное условие '
                'чтобы бот был админом группы или же пользователь заранее нажал в боте старт):')

    @staticmethod
    def get_wrond_target_url():
        return 'Url таргета должен быть ссылкой 🚫'

    @staticmethod
    def get_wrond_target_chat_id_text():
        return 'Вы ввели непраивльный id чата куда будет отправляться результат. Попробуйте еще раз'

    @staticmethod
    def get_cancel_adding_target_text():
        return 'Вы успешно отменили добавление таргета 🤝'

    @staticmethod
    def get_welcome_text():
        return 'Добро пожаловать в бот по поиску обьявлений'

    @staticmethod
    def get_targets_menu_text():
        return 'Меню таргетов'

    @staticmethod
    def get_target_success_text():
        return 'Таргет был успешно добавлен'

