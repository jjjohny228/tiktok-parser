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
    def get_source_channel_url_text() -> str:
        return 'Send source channel url'

    @staticmethod
    def get_wrong_channel_url() -> str:
        return 'You have sent wrong channel url'

    @staticmethod
    def get_add_target_channel_url_text() -> str:
        return 'Send target channel url'

    @staticmethod
    def get_target_channel_apostol_id_text() -> str:
        return 'Send apostol youtube channel id (in apostol app)'

    @staticmethod
    def get_add_channel_success_text() -> str:
        return 'You have successfully added channel'

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
        return 'Welcome to the tiktok bot'

    @staticmethod
    def get_targets_menu_text():
        return 'Меню таргетов'

    @staticmethod
    def get_target_success_text():
        return 'Таргет был успешно добавлен'

    @staticmethod
    def get_all_targets_text(targets: list) -> str:
        result = ''
        for target in targets:
            result += f'{target.id}\n{target.source_channel.url}\n{target.target_channel_url}\n\n'
        return result

