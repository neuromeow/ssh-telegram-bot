from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types.message import ContentType

from bot.misc import IsAdmin, main_menu_keyboard


async def cmd_start(message: types.Message, state: FSMContext):
    if await state.get_state():
        await state.reset_state()
    await message.answer(
        "This bot provides the ability...",
        reply_markup=main_menu_keyboard
    )


async def undefined_request(message: types.Message):
    await message.answer(
        "Undefined request"
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, IsAdmin(), CommandStart, state="*")
    dp.register_message_handler(undefined_request, content_types=ContentType.ANY, state="*")
