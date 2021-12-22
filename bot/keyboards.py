from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def generate_connection_keyboard(
        hostname: str = None, user: str = None, password: str = None, port: str = None
) -> InlineKeyboardMarkup:
    connection_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(f"{'✔' if hostname else '➕'} HostName", callback_data="hostname_option")],
            [InlineKeyboardButton(f"{'✔' if port else '➕'} Port", callback_data="port_option")],
            [InlineKeyboardButton(f"{'✔' if user else '➕'} User", callback_data="user_option")],
            [InlineKeyboardButton(f"{'✔' if password else '➕'} Password", callback_data="password_option")]
        ]
    )
    if hostname or user or password or port:
        connection_keyboard.add(InlineKeyboardButton("➰ Reset", callback_data="reset"))
    if hostname and user and password and port:
        connection_keyboard.add(InlineKeyboardButton("👨🏻‍💻 Connect", callback_data="connect"))
    return connection_keyboard


start_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("⚙ Connect via SSH", callback_data="connection")]
    ]
)
