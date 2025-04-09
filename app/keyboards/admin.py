from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_admin_main_kb() -> ReplyKeyboardMarkup:
    """Створення головної клавіатури адмін-панелі"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Товари"), KeyboardButton(text="👥 Користувачі")],
            [KeyboardButton(text="📋 Замовлення")],
            [KeyboardButton(text="🔙 Назад до меню")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_admin_products_kb() -> ReplyKeyboardMarkup:
    """Клавіатура для управління товарами"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Переглянути товари")],
            [KeyboardButton(text="➕ Додати товар"), KeyboardButton(text="🗑️ Видалити товар")],
            [KeyboardButton(text="🔙 Назад до адмін-меню")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_admin_users_kb() -> ReplyKeyboardMarkup:
    """Клавіатура для управління користувачами"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Переглянути користувачів")],
            [KeyboardButton(text="🗑️ Видалити користувача")],
            [KeyboardButton(text="🔙 Назад до адмін-меню")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_admin_orders_kb() -> ReplyKeyboardMarkup:
    """Клавіатура для управління замовленнями"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Переглянути замовлення")],
            [KeyboardButton(text="🔄 Змінити статус замовлення")],
            [KeyboardButton(text="🔙 Назад до адмін-меню")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_back_to_admin_kb() -> ReplyKeyboardMarkup:
    """Клавіатура з кнопкою повернення до адмін-меню"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Назад до адмін-меню")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_product_management_kb() -> ReplyKeyboardMarkup:
    """Клавіатура для управління товаром"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✏️ Редагувати"), KeyboardButton(text="🗑️ Видалити")],
            [KeyboardButton(text="🔙 Назад до адмін-меню")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_order_status_kb() -> ReplyKeyboardMarkup:
    """Клавіатура для вибору статусу замовлення"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Pending"), KeyboardButton(text="Paid")],
            [KeyboardButton(text="Processing"), KeyboardButton(text="Shipped")],
            [KeyboardButton(text="Delivered"), KeyboardButton(text="Cancelled")],
            [KeyboardButton(text="🔙 Назад до адмін-меню")]
        ],
        resize_keyboard=True
    )
    return keyboard