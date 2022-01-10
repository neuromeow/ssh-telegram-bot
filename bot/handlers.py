from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types.message import ContentType
from aiogram.utils.exceptions import MessageTextIsEmpty

from loguru import logger

from bot.keyboards import generate_configuration_menu_keyboard, start_menu_keyboard
from bot.misc import ConnectionStatus, ConfigurationOptions, IsAdmin, execute_command


async def cmd_start(message: types.Message, state: FSMContext):
    """Resets the current state (if any), sends a welcome message - serves as an entry point for the user."""
    if await state.get_state():
        await state.reset_state()
    await message.answer(
        "This bot provides the ability to connect via Secure Shell (SSH) to the Linux-based machines "
        "using common SSH configuration options: <b>HostName (as IP address), User, Port and Password</b>",
        reply_markup=start_menu_keyboard
    )


async def set_configuration_state(message: types.Message, state: FSMContext):
    """Switches to the state of waiting for the SSH configuration options, generates settings interface."""
    configuration = await state.get_data()
    await message.answer(
        "\n".join(f"<b>{option.title()}:</b> {value}" for option, value in configuration.items())
        if configuration
        else "Configure the options, the connect button will be available after configuring all:",
        reply_markup=generate_configuration_menu_keyboard(**configuration)
    )
    await ConnectionStatus.configuration.set()


async def configuration_menu_button(callback: types.CallbackQuery, state: FSMContext):
    """Reacts to pressing the start menu keyboard button by calling the function to set the SSH configuration state."""
    await set_configuration_state(callback.message, state)
    await callback.answer()


async def option_button(callback: types.CallbackQuery, state: FSMContext):
    """Switches to the state of waiting for the SSH configuration option value that matches the passed callback data."""
    option = callback.data.split('_')[0]
    await callback.message.edit_text(f"Enter the <b>{option}</b>")
    await state.set_state(f"ConfigurationOptions:{option}")


async def enter_option_value(message: types.Message, state: FSMContext):
    """Accepts and updates the value of SSH configuration option corresponding to the passed state."""
    current_state = await state.get_state()
    option = current_state.split(':')[1]
    await update_option_value(option, message, state)


async def update_option_value(option: str, message: types.Message, state: FSMContext) -> None:
    """Sets and updates the value of the passed option in the state data, switches back to the configuration state."""
    configuration = await state.get_data()
    configuration[option] = message.text
    await state.update_data(configuration)
    await set_configuration_state(message, state)


async def reset_button(callback: types.CallbackQuery, state: FSMContext):
    """Resets all user data (SSH configuration options and their values)."""
    await state.reset_data()
    await callback.message.edit_text("The current values of the connection configuration options have been reset")
    await set_configuration_state(callback.message, state)


async def set_command_mode_state(message: types.Message):
    """Switches to the state of waiting for input of predefined bot commands."""
    await message.answer(
        "<b>Now you can use some commands to be executed on the remote server:</b>\n"
        "/whoami to display the name of the currently logged-in user\n"
        "/uptime to find out how long the system is active (running)\n\n"
        "<b>Or switch to interactive mode to enter shell commands yourself in messages to the bot:</b>\n"
        "/interactive to enable/disable interactive mode (when is enabled, the bot commands above don't work)\n\n"
        "<b>Remember that many manipulation capabilities depend on your access level.</b>"
    )
    await ConnectionStatus.command_mode.set()


async def connect_button(callback: types.CallbackQuery, state: FSMContext):
    """Checks the possibility of SSH connection and switches to the state of waiting for input of the bot commands."""
    if len(await state.get_data()) < 4:
        await callback.answer()
    else:
        await callback.message.edit_text("Wait for confirmation of the possibility of SSH connection...")
        try:
            await execute_command(state)
        except Exception as e:
            await callback.message.answer(
                "Sorry, connection is impossible.\n\n"
                "<b>Error:</b>\n"
                f"{e}\n\n"
                "Try changing your connection settings (SSH configuration options):\n"
                "/connect"
            )
        else:
            await set_command_mode_state(callback.message)


async def cmd_whoami(message: types.Message, state: FSMContext):
    """Executes whoami shell command and returns its result."""
    whoami_response = await execute_command(state, command="whoami", response=True)
    await message.answer(whoami_response)


async def cmd_uptime(message: types.Message, state: FSMContext):
    """Executes uptime shell command and returns its result."""
    uptime_response = await execute_command(state, command="uptime", response=True)
    await message.answer(uptime_response)


async def cmd_interactive(message: types.Message, state: FSMContext):
    """Reverts to the previous state or switches to the state of interactive mode depending on the passed state."""
    if await state.get_state() == ConnectionStatus.interactive_mode.state:
        await message.answer("Interactive mode disabled")
        await set_command_mode_state(message)
    else:
        await message.answer("Interactive mode enabled")
        await message.answer(
            "<b>IMPORTANT</b>\n\n"
            "1. Each of your shell commands starts from the user's home directory.\n\n"
            "2. If your shell command returns nothing, this will be reported in the response message.\n\n"
            "3. Also you can execute combine multiple commands in one line "
            "(for example, to solve problems related to the statements above):\n"
            "<b>cd dir1; ls</b> – will show the contents of the directory <b>../dir1/</b>\n"
            "<b>mkdir dir2; cd dir2; touch file; ls -a</b> – these commands will return (the bot will send you back):\n"
            "<b>.\n"
            "..\n"
            "file</b>"
        )
        await ConnectionStatus.next()


async def execute_shell_command(message: types.Message, state: FSMContext):
    """Accepts the user's message and executes it as a shell command, returning the execution result."""
    try:
        shell_command_response = await execute_command(state, command=message.text, response=True)
        await message.answer(shell_command_response)
    except MessageTextIsEmpty:
        await message.answer("stdout/stderr are empty – your command executed but returned nothing")


async def undefined_request(message: types.Message):
    """Replies with a special message for requests for which there are currently no handlers."""
    response = "The command is currently unavailable" if message.text.startswith("/") else "Undefined request"
    await message.answer(response)


async def unexpected_exception(_update: types.Update, exception: Exception):
    """Catches and logs all errors and exceptions."""
    logger.debug(exception)
    return True


def register_handlers(dp: Dispatcher):
    """Registers all bot handlers."""
    dp.register_message_handler(cmd_start, IsAdmin(), CommandStart(), state="*")
    dp.register_message_handler(set_configuration_state, IsAdmin(), commands=["connect"], state="*")
    dp.register_callback_query_handler(configuration_menu_button, Text(equals="configure"))
    dp.register_callback_query_handler(option_button, Text(endswith="option"), state=ConnectionStatus.configuration)
    dp.register_message_handler(enter_option_value, state=ConfigurationOptions.states_names)
    dp.register_callback_query_handler(reset_button, Text(equals="reset"), state=ConnectionStatus.configuration)
    dp.register_callback_query_handler(connect_button, Text(equals="connect"), state=ConnectionStatus.configuration)
    dp.register_message_handler(cmd_whoami, commands=["whoami"], state=ConnectionStatus.command_mode)
    dp.register_message_handler(cmd_uptime, commands=["uptime"], state=ConnectionStatus.command_mode)
    dp.register_message_handler(cmd_interactive, commands=["interactive"], state=ConnectionStatus.command_mode)
    dp.register_message_handler(cmd_interactive, commands=["interactive"], state=ConnectionStatus.interactive_mode)
    dp.register_message_handler(execute_shell_command, state=ConnectionStatus.interactive_mode)
    dp.register_message_handler(undefined_request, IsAdmin(), content_types=ContentType.ANY, state="*")
    dp.register_errors_handler(unexpected_exception)
