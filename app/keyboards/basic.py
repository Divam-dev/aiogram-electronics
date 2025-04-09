from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_currency_kb() -> ReplyKeyboardMarkup:
    """Create currency selection keyboard."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="UAH🇺🇦"), KeyboardButton(text="USD🇺🇸")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Виберіть валюту..."
    )
    return keyboard

def get_menu_kb() -> ReplyKeyboardMarkup:
    """Create simple menu navigation keyboard."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔙 Назад до меню"),
                KeyboardButton(text="🛒 Переглянути кошик")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard