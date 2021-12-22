from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.config import BOT_ADMINS


class ConnectionStatus(StatesGroup):
    configuration = State()


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
