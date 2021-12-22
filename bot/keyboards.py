from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def generate_connection_keyboard(
        host: str = None, username: str = None, password: str = None, port: str = None
) -> InlineKeyboardMarkup:
    connection_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(f"{'✔' if host else '➕'} Host", callback_data="host_field")],
            [InlineKeyboardButton(f"{'✔' if username else '➕'} Username", callback_data="username_field")],
            [InlineKeyboardButton(f"{'✔' if password else '➕'} Password", callback_data="password_field")],
            [InlineKeyboardButton(f"{'✔' if port else '➕'} Port", callback_data="port_field")]
        ]
    )
    return connection_keyboard


start_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("⚙ Connect via SSH", callback_data="configure_connection")]
    ]
)
