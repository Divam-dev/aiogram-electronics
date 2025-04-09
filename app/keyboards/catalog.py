from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.services.db_service import get_category

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

def get_product_inline_kb(product_id: str) -> InlineKeyboardMarkup:
    """Create inline keyboard for buying a product."""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="🛒 Купити", 
        callback_data=f"buy_{product_id}"
    ))
    return builder.as_markup()