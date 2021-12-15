from aiogram import Dispatcher, types
from aiogram.types.message import ContentType


async def undefined_request(message: types.Message):
    await message.answer(
        "Undefined request"
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(undefined_request, content_types=ContentType.ANY, state="*")
