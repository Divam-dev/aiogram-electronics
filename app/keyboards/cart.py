from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_cart_kb() -> ReplyKeyboardMarkup:
    """Create keyboard for cart management."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Назад до меню")],
            [KeyboardButton(text="💵 Оформити замовлення")],
            [KeyboardButton(text="🗑️ Очистити кошик")]
        ],
        resize_keyboard=True
    )
    return keyboard