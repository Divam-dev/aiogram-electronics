from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_cart_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Назад до меню")],
            [KeyboardButton(text="💵 Оформити замовлення")],
            [KeyboardButton(text="🗑️ Очистити кошик")]
        ],
        resize_keyboard=True
    )
    return keyboard