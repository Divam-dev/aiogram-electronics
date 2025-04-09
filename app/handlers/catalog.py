from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from app.keyboards import get_currency_kb, get_categories_kb, get_product_inline_kb, get_menu_kb
from app.data_handler import (
    get_category, get_products_by_category, get_product_by_id,
    currency_convert, customer_exists, add_new_customer
)
from app.handlers.common import OrderStates, carts
from app.handlers.cart import view_cart

router = Router()

@router.message(CommandStart())
@router.message(Command("help"))
async def cmd_start_or_help(message: Message, state: FSMContext):
    chat_id = message.chat.id
    
    # Check if customer exists
    if customer_exists(chat_id):
        # If customer exists, skip currency selection
        await send_categories_menu(message, state)
        return
    
    # If new customer, add them to database and ask for currency
    if message.text == "/start":
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        add_new_customer(chat_id, first_name, last_name)
        
        text = f"Вітаю {first_name}, я допоможу тобі з вибором електроніки 📱.\nВиберіть валюту:"
    else:
        text = "Виберіть валюту:"
    
    await state.set_state(OrderStates.choosing_currency)
    await message.answer(text, reply_markup=get_currency_kb())

@router.message(OrderStates.choosing_currency, F.text.in_(["USD🇺🇸", "UAH🇺🇦"]))
async def process_currency_selection(message: Message, state: FSMContext):
    await state.update_data(currency=message.text)
    currency_code = "UAH" if message.text == "UAH🇺🇦" else "USD"
    await state.update_data(currency_code=currency_code)
    await message.answer(f"Ви обрали {message.text}")
    await send_categories_menu(message, state)

async def send_categories_menu(message: Message, state: FSMContext):
    await state.set_state(OrderStates.choosing_category)
    await message.answer(
        "Ви знаходитесь в меню, виберіть бажану категорію", 
        reply_markup=get_categories_kb()
    )

@router.message(OrderStates.choosing_category, F.text.in_(get_category()))
async def process_category_selection(message: Message, state: FSMContext):
    category = message.text
    await state.update_data(category=category)
    await display_products(message, state, category)

async def display_products(message: Message, state: FSMContext, category):
    await state.set_state(OrderStates.viewing_products)
    
    products = get_products_by_category(category)
    
    await message.answer(
        f"Знайдено {len(products)} товарів в категорії {category}:", 
        reply_markup=get_menu_kb()
    )
    
    data = await state.get_data()
    currency = data.get("currency", "UAH🇺🇦")
    usd_rate = float(currency_convert()) if currency == "USD🇺🇸" else 1
    currency_symbol = "$" if currency == "USD🇺🇸" else "₴"
    
    for product in products:
        product_id = product[0]
        name = product[1]
        price = round(float(product[3]) / usd_rate, 2)
        stock = product[4]
        full_name = product[5] or name
        image_url = product[6]
        
        product_info = (
            f"Назва: {full_name}\n"
            f"Категорія: {category}\n"
            f"Ціна: {price} {currency_symbol}\n"
            f"В наявності: {stock} шт."
        )
        
        if image_url:
            await message.answer_photo(
                image_url,
                product_info,
                reply_markup=get_product_inline_kb(product_id)
            )
        else:
            await message.answer(
                product_info,
                reply_markup=get_product_inline_kb(product_id)
            )

@router.message(F.text == "🔙 Назад до меню")
async def back_to_menu(message: Message, state: FSMContext):
    await send_categories_menu(message, state)

@router.callback_query(F.data.startswith("buy_"))
async def process_buy(callback: CallbackQuery, state: FSMContext):
    product_id = callback.data.split("_")[1]
    chat_id = callback.message.chat.id
    
    product = get_product_by_id(product_id)
    if product:
        product_name = product[1]
        product_price = float(product[3])
        
        if chat_id not in carts:
            carts[chat_id] = {}
        
        if product_name in carts[chat_id]:
            carts[chat_id][product_name]["quantity"] += 1
        else:
            carts[chat_id][product_name] = {"quantity": 1, "price": product_price}
        
        await callback.answer(f"✅ {product_name} додано до кошика!")
    else:
        await callback.answer("❌ Помилка! Товар не знайдено.")