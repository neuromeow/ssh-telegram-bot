from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import BoundFilter

from bot.config import BOT_ADMINS


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return str(message.from_user.id) in BOT_ADMINS


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("/connection", "SSH configure and connect"),
            types.BotCommand("/reboot", "Reboot server"),
            types.BotCommand("/uptime", "Check status"),
            types.BotCommand("/interactive", "Interactive mode")
        ]
    )
