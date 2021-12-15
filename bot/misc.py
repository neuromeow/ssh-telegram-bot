from aiogram import Dispatcher, types


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("/ssh", "Set up SSH connection"),
            types.BotCommand("/reboot", "Reboot server"),
            types.BotCommand("/uptime", "Check status"),
            types.BotCommand("/interactive", "Interactive mode")
        ]
    )
