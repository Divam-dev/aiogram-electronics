from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.data_handler import get_category

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

def get_categories_kb() -> ReplyKeyboardMarkup:
    """Create categories keyboard with cart button."""
    builder = ReplyKeyboardBuilder()
    
    for category in get_category():
        builder.add(KeyboardButton(text=category))
    
    builder.add(KeyboardButton(text="🛒 Переглянути кошик"))
    
    return builder.adjust(2).as_markup(
        resize_keyboard=True,
        input_field_placeholder="Виберіть категорію..."
    )

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

def get_product_inline_kb(product_id: str) -> InlineKeyboardMarkup:
    """Create inline keyboard for buying a product."""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="🛒 Купити", 
        callback_data=f"buy_{product_id}"
    ))
    return builder.as_markup()

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