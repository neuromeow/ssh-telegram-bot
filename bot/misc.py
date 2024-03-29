from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

import paramiko

from bot.config import BOT_ADMINS


class ConnectionStatus(StatesGroup):
    """Class for representing the connection status."""
    configuration = State()
    command_mode = State()
    interactive_mode = State()


class ConfigurationOptions(StatesGroup):
    """Class for representing the configuration options for establishing a connection."""
    hostname = State()
    port = State()
    username = State()
    password = State()


class IsAdmin(BoundFilter):
    """A filter class to check if the sender of a Telegram message is an admin."""

    async def check(self, message: types.Message) -> bool:
        return str(message.from_user.id) in BOT_ADMINS


async def set_bot_commands(dp: Dispatcher):
    """Sets the bot commands to the bot user interface."""
    await dp.bot.set_my_commands(
        [
            types.BotCommand("/connect", "configure and connect via SSH"),
            types.BotCommand("/whoami", "whoami command"),
            types.BotCommand("/uptime", "uptime command"),
            types.BotCommand("/interactive", "enable/disable interactive mode")
        ]
    )


async def ssh_connection(state: FSMContext, command: str = None, response: bool = False) -> [None, str]:
    """Connects via SSH and immediately disconnects, if necessary, executes the command and returns its result."""
    configuration = await state.get_data()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(**configuration)
    if command:
        stdin, stdout, stderr = client.exec_command(command)
        if response:
            command_response = (stdout.read() + stderr.read()).decode("utf-8").strip()
            client.close()
            return command_response
    client.close()
