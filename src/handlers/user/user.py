from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from src.database.user import create_user_if_not_exist, create_channel_if_not_exist, \
    create_target_if_not_exist, create_video_if_not_exist, get_all_targets, get_target_by_id, delete_target_by_id
from src.utils import send_typing_action
from src.handlers.user.kb import Keyboards
from config import Config
from src.utils import logger
from src.create_bot import bot
from src.misc.user_states import UserChannelInputting, DeleteChannelInputting
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

    @staticmethod
    async def send_database() -> None:
        dump_path = Config.DATABASE_PATH
        for admin_id in {*Config.ADMIN_IDS}:
            with open(dump_path, 'rb') as database_file:
                await bot.send_document(admin_id, database_file)

    @staticmethod
    async def send_posted_video_message(target_channel_url: str) -> None:
        for admin_id in {*Config.ADMIN_IDS}:
            await bot.send_message(admin_id, f'Video was posted on channel {target_channel_url}')




class Handlers:
    @staticmethod
    async def __handle_add_channel_button(callback: CallbackQuery, state: FSMContext):
        await callback.message.answer(text=Messages.get_source_channel_url_text(),
                             reply_markup=Keyboards.get_cancel_adding_channel_markup())
        await state.set_state(UserChannelInputting.source_channel_url)

    @staticmethod
    async def __handle_source_channel_url(message: Message, state: FSMContext):
        if not message.text.startswith("https://"):
            await message.answer(Messages.get_wrong_channel_url())
        else:
            await state.update_data(source_channel_url=message.text.split("?")[0])
            await message.answer(Messages.get_add_target_channel_url_text())
            await state.set_state(UserChannelInputting.target_channel_url)

    @staticmethod
    async def __handle_target_channel_url(message: Message, state: FSMContext):
        if not message.text.startswith("https://"):
            await message.answer(Messages.get_wrond_target_url())
        else:
            await state.update_data(target_channel_url=message.text)
            await message.answer(Messages.get_target_channel_apostol_id_text())
            await state.set_state(UserChannelInputting.target_channel_apostol_id)

    @staticmethod
    async def __handle_target_channel_apostol_id(message: Message, state: FSMContext):
        from src.content_functions.parser import Parser

        await state.update_data(target_channel_apostol_id=message.text)

        # Save channel and target
        data = await state.get_data()
        source_channel_url = data.get("source_channel_url")
        target_channel_url = data.get("target_channel_url")
        target_channel_apostol_id = data.get("target_channel_apostol_id")

        create_channel_if_not_exist(source_channel_url)
        new_target = create_target_if_not_exist(source_channel_url, target_channel_url, target_channel_apostol_id)
        if new_target:
            last_channel_videos = await Parser().get_last_channel_videos(new_target.source_channel.name)
            for last_channel_video in last_channel_videos:
                create_video_if_not_exist(last_channel_video, new_target.source_channel)
        await message.answer(Messages.get_add_channel_success_text(), reply_markup=Keyboards.get_menu_markup())
        await state.finish()

    @staticmethod
    async def __handle_cancel_adding_channel(message: Message, state: FSMContext):
        await message.answer(Messages.get_cancel_adding_target_text(), reply_markup=Keyboards.get_menu_markup())
        await state.finish()

    @staticmethod
    async def __handle_main_menu(message: Message):
        await message.answer('🏠', reply_markup=Keyboards.get_menu_markup())

    @staticmethod
    async def __handle_channel_menu(message: Message):
        targets = get_all_targets()
        print(targets)
        if targets:
            await message.answer(text=Messages.get_all_targets_text(targets),
                                 disable_web_page_preview=True,
                                 reply_markup=Keyboards.get_channels_markup(has_channels=True))
        else:
            await message.answer(text='You dont have any targets',
                                 disable_web_page_preview=True,
                                 reply_markup=Keyboards.get_channels_markup(has_channels=False))

    @staticmethod
    async def __handle_delete_target(callback: CallbackQuery, state: FSMContext):
        await callback.message.answer('Send channel id to delete it',
                                      reply_markup=Keyboards.get_cancel_adding_channel_markup())
        await state.set_state(DeleteChannelInputting.channel_id)
        await callback.answer()

    @staticmethod
    async def __handle_delete_target_id(message: Message, state: FSMContext):
        if not message.text.isdigit():
            await message.answer('You should enter a number')
            return
        target = get_target_by_id(message.text)
        if not target:
            await message.answer('You entered invalid target id')
            return
        delete_target_by_id(target.id)
        await message.answer(f'Target with id {target.id} was deleted successfully',
                             reply_markup=Keyboards.get_menu_markup())
        await state.finish()

    @staticmethod
    async def __handle_start_command(message: Message, state: FSMContext) -> None:
        await state.finish()
        await send_typing_action(message)

        create_user_if_not_exist(
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.first_name,
            telegram_id=message.from_id,
        )

        await message.answer(
            text=Messages.get_welcome_text(),
            reply_markup=Keyboards.get_menu_markup()
            )


    @classmethod
    def register_user_handlers(cls, dp: Dispatcher) -> None:
        dp.register_message_handler(cls.__handle_start_command, CommandStart(), state=None)
        dp.register_message_handler(cls.__handle_cancel_adding_channel, state='*', text='Cancel')
        dp.register_callback_query_handler(cls.__handle_add_channel_button,
                                    lambda c: c.data == 'add_channel',
                                    state=None)
        dp.register_message_handler(cls.__handle_source_channel_url,
                                           state=UserChannelInputting.source_channel_url)
        dp.register_message_handler(cls.__handle_target_channel_url,
                                    state=UserChannelInputting.target_channel_url)
        dp.register_message_handler(cls.__handle_target_channel_apostol_id,
                                    state=UserChannelInputting.target_channel_apostol_id)
        dp.register_message_handler(cls.__handle_channel_menu,
                                    text='Channels')
        dp.register_callback_query_handler(cls.__handle_delete_target,
                                           lambda c: c.data == 'delete_channel',
                                           state=None)
        dp.register_message_handler(cls.__handle_delete_target_id,
                                           state=DeleteChannelInputting.channel_id)



def register_user_handlers(dp: Dispatcher):
    Handlers.register_user_handlers(dp)

