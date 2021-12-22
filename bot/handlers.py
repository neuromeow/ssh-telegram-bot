from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types.message import ContentType

from bot.keyboards import start_menu_keyboard, generate_connection_keyboard
from bot.misc import IsAdmin


async def cmd_start(message: types.Message, state: FSMContext):
    if await state.get_state():
        await state.reset_state()
    await message.answer(
        "This bot provides the ability...",
        reply_markup=start_menu_keyboard
    )


async def generate_connection_menu(message: types.Message, state: FSMContext):
    current_data = await state.get_data()
    await message.answer(
        "\n".join(f"{key}: {current_data[key]}" for key in current_data)
        if current_data else "Connect button will appear after all settings have been added...",
        reply_markup=generate_connection_keyboard(**current_data)
    )


async def cmd_connection(message: types.Message, state: FSMContext):
    # if await state.get_state():
    #     pass
    await generate_connection_menu(message, state)


async def configure_connection_button(callback: types.CallbackQuery, state: FSMContext):
    await generate_connection_menu(callback.message, state)
    await callback.answer()


async def undefined_request(message: types.Message):
    await message.answer(
        "Undefined request"
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, IsAdmin(), CommandStart(), state="*")
    dp.register_message_handler(cmd_connection, IsAdmin(), commands=["connection"], state="*")
    dp.register_callback_query_handler(configure_connection_button, Text(equals="configure_connection"))
    dp.register_message_handler(undefined_request, content_types=ContentType.ANY, state="*")
