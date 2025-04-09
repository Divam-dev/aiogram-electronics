from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_delivery_method_kb() -> ReplyKeyboardMarkup:
    """Create keyboard for delivery method selection."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚚 Оплатити зараз")],
            [KeyboardButton(text="🏪 Самовивіз")],
            [KeyboardButton(text="🔙 Назад до кошику")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_confirmation_kb() -> ReplyKeyboardMarkup:
    """Клавіатура для підтвердження дії"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Підтвердити"), KeyboardButton(text="❌ Скасувати")]
        ],
        resize_keyboard=True
    )
    return keyboard