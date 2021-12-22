from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentType

from bot.keyboards import start_menu_keyboard, generate_connection_keyboard
from bot.misc import IsAdmin


class ConnectionStatus(StatesGroup):
    configuration = State()


class ConfigurationOptions(StatesGroup):
    hostname = State()
    port = State()
    user = State()
    password = State()


async def cmd_start(message: types.Message, state: FSMContext):
    if await state.get_state():
        await state.reset_state()
    await message.answer(
        "This bot provides the ability...",
        reply_markup=start_menu_keyboard
    )


async def generate_connection_menu(message: types.Message, state: FSMContext):
    configuration = await state.get_data()
    await message.answer(
        "\n".join(f"{option}: {value}" for option, value in configuration.items())
        if configuration else "Connect button will appear after all settings have been added...",
        reply_markup=generate_connection_keyboard(**configuration)
    )
    await ConnectionStatus.configuration.set()


async def configure_connection_button(callback: types.CallbackQuery, state: FSMContext):
    await generate_connection_menu(callback.message, state)
    await callback.answer()


async def option_button(callback: types.CallbackQuery, state: FSMContext):
    """Universal function of the invitation to input SSH configuration option corresponding to the button."""
    option = callback.data.split('_')[0]
    await callback.message.edit_text(f"Enter the {option}.")
    await state.set_state(f"ConfigurationOptions:{option}")


async def enter_option_value(message: types.Message, state: FSMContext):
    """Universal function for entering SSH configuration option value corresponding to the state."""
    current_state = await state.get_state()
    option = current_state.split(':')[1]
    await update_option_value(option, message, state)


async def update_option_value(option: str, message: types.Message, state: FSMContext) -> None:
    if len(message.text) == 4096:
        await message.reply(f"Please note that this message will be added as {option} value.")
    configuration = await state.get_data()
    configuration[option] = message.text
    await state.update_data(configuration)
    await generate_connection_menu(message, state)


async def undefined_request(message: types.Message):
    await message.answer(
        "Undefined request"
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, IsAdmin(), CommandStart(), state="*")
    dp.register_message_handler(generate_connection_menu, IsAdmin(), commands=["connection"], state="*")
    dp.register_callback_query_handler(configure_connection_button, Text(equals="connection"))
    dp.register_callback_query_handler(option_button, Text(endswith="option"), state=ConnectionStatus.configuration)
    dp.register_message_handler(enter_option_value, state=ConfigurationOptions.states_names)
    dp.register_message_handler(undefined_request, content_types=ContentType.ANY, state="*")
