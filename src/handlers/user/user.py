import asyncio
import re

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import CallbackQuery, Message, Chat
from aiogram.utils import exceptions
from aiogram.utils.exceptions import ChatNotFound, BotBlocked

from src.database.user import create_user_if_not_exist, create_target, get_user_targets
from src.utils import send_typing_action
from .kb import Keyboards
# from src.misc import UserDataInputting
from .messages import Messages
from src.filters.filter_func import check_is_admin
from src.handlers.admin.admin import send_admin_menu
# from .kb import Keyboards
from config import Config
from src.utils import logger
from src.create_bot import bot
from src.misc.user_states import UserTargetInputting
from src.handlers.user.messages import Messages


class Utils:
    @staticmethod
    async def is_valid_chat_id(chat_id: int) -> bool:
        try:
            chat = await bot.get_chat(chat_id)
            logger.info(chat)
            return True
        except Exception as e:
            logger.error(f'Some error occurred: {e}')
            return False


class Handlers:
    @staticmethod
    async def __handle_add_target_button(message: Message, state: FSMContext):
        await message.answer(Messages.get_add_taget_name_text(), reply_markup=Keyboards.get_cancel_target_markup())
        await state.set_state(UserTargetInputting.target_name)

    @staticmethod
    async def __handle_taget_name(message: Message, state: FSMContext):
        await state.update_data(target_name=message.text)
        await message.answer(Messages.get_add_taget_url_text())
        await state.set_state(UserTargetInputting.target_url)

    @staticmethod
    async def __handle_taget_url(message: Message, state: FSMContext):
        if not message.text.startswith("https://"):
            await message.answer(Messages.get_wrond_target_url())
        else:
            await state.update_data(target_url=message.text)
            await message.answer(Messages.get_add_taget_chat_id_text())
            await state.set_state(UserTargetInputting.target_chat_id)

    @staticmethod
    async def __handle_chat_id(message: Message, state: FSMContext):
        if not await Utils.is_valid_chat_id(message.text):
            await message.answer(Messages.get_wrond_target_chat_id_text())
        else:
            await state.update_data(chat_id=message.text)

            # Save target
            data = await state.get_data()
            target_name = data.get("target_name")
            target_url = data.get("target_url")
            chat_id = data.get("chat_id")

            create_target(message.from_user.id, target_name, target_url, chat_id)
            await message.answer(Messages.get_target_success_text(), reply_markup=Keyboards.get_targets_menu())
            await state.finish()

    @staticmethod
    async def __handle_cancel_adding_target(message: Message, state: FSMContext):
        await message.answer(Messages.get_cancel_adding_target_text(), reply_markup=Keyboards.get_targets_menu())
        await state.finish()

    @staticmethod
    async def __handle_main_menu(message: Message):
        await message.answer('🏠', reply_markup=Keyboards.get_main_menu_markup(message))

    @staticmethod
    async def __handle_my_targets(message: Message):
        if get_user_targets(message.from_user.id):
            await message.answer(text='Чтобы редактировать таргет нажмите на один из них',
                                 reply_markup=Keyboards.get_my_targets_markup(message.from_user.id))
        else:
            await message.answer('У вас нет тергетов')

    @staticmethod
    async def __handle_targets_menu_callback(callback: CallbackQuery):
        await callback.answer()
        await callback.message.delete()
        await callback.message.answer('Меню таргетов', reply_markup=Keyboards.get_targets_menu())

    @staticmethod
    async def __handle_start_command(message: Message, state: FSMContext) -> None:
        await state.finish()
        if check_is_admin(message):
            await send_admin_menu(message)
        else:
            await send_typing_action(message)

            create_user_if_not_exist(
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.first_name,
                telegram_id=message.from_id,
            )

            await message.answer(
                text=Messages.get_welcome_text(),
                reply_markup=Keyboards.get_main_menu_markup(message)
            )
    @staticmethod
    async def __handle_tagets_menu(message: Message):
        await message.answer(text=Messages.get_targets_menu_text(),
                             reply_markup=Keyboards.get_targets_menu())

    @staticmethod
    async def __change_target_page(callback_query: CallbackQuery):
        page = int(callback_query.data.split("_")[1])
        await callback_query.message.edit_reply_markup(
            reply_markup=Keyboards.get_my_targets_markup(callback_query.from_user.id, page))
        await callback_query.answer()


    @classmethod
    def register_user_handlers(cls, dp: Dispatcher) -> None:
        dp.register_message_handler(cls.__handle_start_command, CommandStart(), state=None)
        dp.register_message_handler(cls.__handle_cancel_adding_target, state='*', text='Отменить добавление таргета')
        dp.register_message_handler(cls.__handle_add_target_button, text='Добавить таргет ➕', state=None)
        dp.register_message_handler(cls.__handle_taget_name, state=UserTargetInputting.target_name)
        dp.register_message_handler(cls.__handle_taget_url, state=UserTargetInputting.target_url)
        dp.register_message_handler(cls.__handle_chat_id, state=UserTargetInputting.target_chat_id)
        dp.register_message_handler(cls.__handle_tagets_menu, text='Таргеты 🚀')
        dp.register_message_handler(cls.__handle_main_menu, text='Назад в главное меню  ⬅️')
        dp.register_callback_query_handler(cls.__change_target_page, lambda c: c.data.startswith("page_") and c.data.endswith("target"))
        dp.register_callback_query_handler(cls.__handle_targets_menu_callback,
                                           lambda c: c.data == 'my_targets_menu')
        dp.register_message_handler(cls.__handle_my_targets, text='Мои таргеты')
        # dp.register_callback_query_handler(__handle_next_signal_callback, text='mines_next_signal')
        # dp.register_callback_query_handler(__handle_menu_callback, text='mines_menu')
        # dp.register_callback_query_handler(__handle_instruction_callback, text='mines_instruction_menu')


def register_user_handlers(dp: Dispatcher):
    Handlers.register_user_handlers(dp)
# async def __handle_next_signal_callback(callback: CallbackQuery):
#     # Удаляем сообщение
#     menu_owner = callback.data.split('_')[0]
#     await callback.answer(text=MinesMessages.get_loading())
#     await callback.message.delete()
#     msg = await callback.message.answer('⌛️ Waiting...')
#     delay_seconds = random.uniform(2, 3)
#
#     await asyncio.sleep(delay_seconds)
#     await msg.delete()
#
#     if get_user_1win_id(callback.message.chat.id):
#         new_photo = MinesMessages.get_random_signal()
#
#         await callback.message.answer_photo(photo=new_photo,
#                                             caption=MinesMessages.get_signal_text(),
#                                             reply_markup=MinesKeyboards.get_signal_markup())
#     else:
#         await callback.message.answer_photo(
#             caption=CommonMessages.get_registration_text(callback.message.chat.first_name),
#             photo=CommonMessages.get_registration_explanation_photo(),
#             reply_markup=CommonKeyboards.get_registration_menu(menu_owner)
#         )
#     await callback.answer()
#
#
# async def __handle_menu_callback(callback: CallbackQuery):
#     await callback.message.delete()
#     await callback.message.answer_photo(photo=MinesMessages.get_menu_photo(),
#                                         caption=MinesMessages.get_menu_text(),
#                                         reply_markup=MinesKeyboards.get_menu_markup())
#     await callback.answer()
#
#
# async def __handle_instruction_callback(callback: CallbackQuery):
#     menu_owner = callback.data.split('_')[0]
#     await callback.message.delete()
#
#     await callback.message.answer_video(
#         video=MinesMessages.get_instruction_video(),
#         caption=MinesMessages.get_instruction_text(),
#         reply_markup=CommonKeyboards.get_instruction_menu(menu_owner)
#     )

