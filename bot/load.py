from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from loguru import logger

from bot.config import BOT_TOKEN
from bot.handlers import register_handlers
from bot.misc import set_default_commands


async def on_startup(dp: Dispatcher):
    register_handlers(dp)
    await set_default_commands(dp)
    logger.info("Telegram bot for SSH connection launched.")


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.info("Telegram bot for SSH connection launched finished.")


def main():
    bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    storage = MemoryStorage()
    bot_dp = Dispatcher(bot, storage=storage)
    executor.start_polling(bot_dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
