from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

import asyncio

from loguru import logger

import paramiko

from bot.config import BOT_ADMINS


class ConnectionStatus(StatesGroup):
    configuration = State()
    commands = State()


class ConfigurationOptions(StatesGroup):
    hostname = State()
    port = State()
    user = State()
    password = State()


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return str(message.from_user.id) in BOT_ADMINS


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("/connect", "SSH configure and connect"),
            types.BotCommand("/reboot", "Reboot server"),
            types.BotCommand("/uptime", "Check status"),
            types.BotCommand("/interactive", "Interactive mode")
        ]
    )


def execute_command(
        hostname: str, user: str, password: str, port: int, command: str = None, response: bool = False
) -> [None, str]:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, username=user, password=password, port=port)
    if command:
        stdin, stdout, stderr = client.exec_command(command)
        if response:
            command_response = (stdout.read() + stderr.read()).decode("utf-8").strip()
            client.close()
            return command_response
    client.close()
