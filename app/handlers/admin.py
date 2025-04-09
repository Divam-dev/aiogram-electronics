from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import sqlite3

from app.keyboards import (
    get_admin_main_kb, get_admin_products_kb, get_admin_users_kb, 
    get_admin_orders_kb, get_back_to_admin_kb, get_product_management_kb,
    get_order_status_kb, get_confirmation_kb
)

# Список ID адміністраторів
ADMIN_IDS = [545363905]  # Замініть на реальні ID адміністраторів

router = Router()

class AdminStates(StatesGroup):
    main_menu = State()
    
    # Продукти
    products_menu = State()
    adding_product = State()
    adding_product_name = State()
    adding_product_category = State()
    adding_product_price = State()
    adding_product_stock = State()
    adding_product_fullname = State()
    adding_product_image = State()
    deleting_product = State()
    
    # Користувачі
    users_menu = State()
    deleting_user = State()
    
    # Замовлення
    orders_menu = State()
    changing_order_status = State()
    confirm_action = State()

def is_admin(user_id):
    """Перевірка чи є користувач адміністратором"""
    return user_id in ADMIN_IDS

@router.message(Command("admin"))
async def admin_command(message: Message, state: FSMContext):
    """Обробка команди /admin"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.answer("❌ У вас немає прав доступу до адмін-панелі.")
        return
    
    await message.answer(
        "👑 Ласкаво просимо до адмін-панелі.\nВиберіть розділ:",
        reply_markup=get_admin_main_kb()
    )
    await state.set_state(AdminStates.main_menu)

# --- ОСНОВНЕ МЕНЮ ---

@router.message(AdminStates.main_menu, F.text == "📦 Товари")
async def products_menu(message: Message, state: FSMContext):
    """Обробка вибору розділу товарів"""
    await message.answer(
        "📦 Управління товарами. Виберіть дію:",
        reply_markup=get_admin_products_kb()
    )
    await state.set_state(AdminStates.products_menu)

@router.message(AdminStates.main_menu, F.text == "👥 Користувачі")
async def users_menu(message: Message, state: FSMContext):
    """Обробка вибору розділу користувачів"""
    await message.answer(
        "👥 Управління користувачами. Виберіть дію:",
        reply_markup=get_admin_users_kb()
    )
    await state.set_state(AdminStates.users_menu)

@router.message(AdminStates.main_menu, F.text == "📋 Замовлення")
async def orders_menu(message: Message, state: FSMContext):
    """Обробка вибору розділу замовлень"""
    await message.answer(
        "📋 Управління замовленнями. Виберіть дію:",
        reply_markup=get_admin_orders_kb()
    )
    await state.set_state(AdminStates.orders_menu)

@router.message(F.text == "🔙 Назад до адмін-меню")
async def back_to_admin_menu(message: Message, state: FSMContext):
    """Повернення до головного адмін-меню"""
    await message.answer(
        "👑 Адмін-панель. Виберіть розділ:",
        reply_markup=get_admin_main_kb()
    )
    await state.set_state(AdminStates.main_menu)

# --- УПРАВЛІННЯ ТОВАРАМИ ---

@router.message(AdminStates.products_menu, F.text == "📋 Переглянути товари")
async def view_products(message: Message, state: FSMContext):
    """Перегляд всіх товарів"""
    try:
        conn = sqlite3.connect('electronics_store.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        conn.close()
        
        if not products:
            await message.answer(
                "❌ Товари не знайдено.", 
                reply_markup=get_admin_products_kb()
            )
            return
        
        for product in products:
            product_info = (
                f"ID: {product[0]}\n"
                f"Назва: {product[1]}\n"
                f"Категорія: {product[2]}\n"
                f"Ціна: {product[3]} грн\n"
                f"Кількість: {product[4]} шт\n"
                f"Повна назва: {product[5] or '-'}\n"
                f"URL зображення: {product[6] or '-'}"
            )
            
            await message.answer(product_info)
            
        await message.answer(
            "✅ Список всіх товарів відображено.",
            reply_markup=get_admin_products_kb()
        )
    
    except Exception as e:
        await message.answer(
            f"❌ Помилка: {str(e)}",
            reply_markup=get_admin_products_kb()
        )

@router.message(AdminStates.products_menu, F.text == "➕ Додати товар")
async def add_product_start(message: Message, state: FSMContext):
    """Початок процесу додавання товару"""
    await message.answer(
        "Введіть коротку назву товару:",
        reply_markup=get_back_to_admin_kb()
    )
    await state.set_state(AdminStates.adding_product_name)

@router.message(AdminStates.adding_product_name)
async def add_product_name(message: Message, state: FSMContext):
    """Обробка назви нового товару"""
    await state.update_data(product_name=message.text)
    await message.answer("Вкажіть категорію товару:")
    await state.set_state(AdminStates.adding_product_category)

@router.message(AdminStates.adding_product_category)
async def add_product_category(message: Message, state: FSMContext):
    """Обробка категорії нового товару"""
    await state.update_data(product_category=message.text)
    await message.answer("Вкажіть ціну товару (лише число):")
    await state.set_state(AdminStates.adding_product_price)

@router.message(AdminStates.adding_product_price)
async def add_product_price(message: Message, state: FSMContext):
    """Обробка ціни нового товару"""
    try:
        price = float(message.text)
        await state.update_data(product_price=price)
        await message.answer("Вкажіть кількість товару на складі (ціле число):")
        await state.set_state(AdminStates.adding_product_stock)
    except ValueError:
        await message.answer("❌ Введіть коректну ціну (лише число):")

@router.message(AdminStates.adding_product_stock)
async def add_product_stock(message: Message, state: FSMContext):
    """Обробка кількості нового товару"""
    try:
        stock = int(message.text)
        await state.update_data(product_stock=stock)
        await message.answer("Введіть повну назву товару (або '-' якщо немає):")
        await state.set_state(AdminStates.adding_product_fullname)
    except ValueError:
        await message.answer("❌ Введіть коректну кількість (ціле число):")

@router.message(AdminStates.adding_product_fullname)
async def add_product_fullname(message: Message, state: FSMContext):
    """Обробка повної назви нового товару"""
    fullname = None if message.text == '-' else message.text
    await state.update_data(product_fullname=fullname)
    await message.answer("Введіть URL зображення товару (або '-' якщо немає):")
    await state.set_state(AdminStates.adding_product_image)

@router.message(AdminStates.adding_product_image)
async def add_product_image(message: Message, state: FSMContext):
    """Завершення додавання товару"""
    image_url = None if message.text == '-' else message.text
    data = await state.get_data()
    
    try:
        conn = sqlite3.connect('electronics_store.db')
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO Products (name, category, price, stock, fullname, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data['product_name'],
                data['product_category'],
                data['product_price'],
                data['product_stock'],
                data['product_fullname'],
                image_url
            )
        )
        
        conn.commit()
        conn.close()
        
        await message.answer(
            f"✅ Товар успішно додано: {data['product_name']}",
            reply_markup=get_admin_products_kb()
        )
        await state.set_state(AdminStates.products_menu)
        
    except Exception as e:
        await message.answer(
            f"❌ Помилка при додаванні товару: {str(e)}",
            reply_markup=get_admin_products_kb()
        )
        await state.set_state(AdminStates.products_menu)

@router.message(AdminStates.products_menu, F.text == "🗑️ Видалити товар")
async def delete_product_start(message: Message, state: FSMContext):
    """Початок процесу видалення товару"""
    await message.answer(
        "Введіть ID товару для видалення:",
        reply_markup=get_back_to_admin_kb()
    )
    await state.set_state(AdminStates.deleting_product)

@router.message(AdminStates.deleting_product)
async def delete_product(message: Message, state: FSMContext):
    """Видалення товару за ID"""
    try:
        product_id = int(message.text)
        
        conn = sqlite3.connect('electronics_store.db')
        cursor = conn.cursor()
        
        # Перевіряємо, чи існує товар з таким ID
        cursor.execute("SELECT name FROM Products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            await message.answer(
                f"❌ Товар з ID {product_id} не знайдено.",
                reply_markup=get_admin_products_kb()
            )
            await state.set_state(AdminStates.products_menu)
            conn.close()
            return
        
        product_name = product[0]
        
        # Видаляємо товар
        cursor.execute("DELETE FROM Products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()
        
        await message.answer(
            f"✅ Товар '{product_name}' (ID: {product_id}) успішно видалено.",
            reply_markup=get_admin_products_kb()
        )
        await state.set_state(AdminStates.products_menu)
        
    except ValueError:
        await message.answer(
            "❌ Введіть коректний ID товару (ціле число):",
            reply_markup=get_back_to_admin_kb()
        )
    except Exception as e:
        await message.answer(
            f"❌ Помилка при видаленні товару: {str(e)}",
            reply_markup=get_admin_products_kb()
        )
        await state.set_state(AdminStates.products_menu)

# --- УПРАВЛІННЯ КОРИСТУВАЧАМИ ---

@router.message(AdminStates.users_menu, F.text == "📋 Переглянути користувачів")
async def view_users(message: Message, state: FSMContext):
    """Перегляд всіх користувачів"""
    try:
        conn = sqlite3.connect('electronics_store.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customers")
        users = cursor.fetchall()
        conn.close()
        
        if not users:
            await message.answer(
                "❌ Користувачів не знайдено.", 
                reply_markup=get_admin_users_kb()
            )
            return
        
        for user in users:
            user_info = (
                f"ID: {user[0]}\n"
                f"Chat ID: {user[1]}\n"
                f"Ім'я: {user[2]}\n"
                f"Прізвище: {user[3] or '-'}\n"
                f"Телефон: {user[4] or '-'}\n"
                f"Email: {user[5] or '-'}"
            )
            
            await message.answer(user_info)
            
        await message.answer(
            "✅ Список всіх користувачів відображено.",
            reply_markup=get_admin_users_kb()
        )
    
    except Exception as e:
        await message.answer(
            f"❌ Помилка: {str(e)}",
            reply_markup=get_admin_users_kb()
        )

@router.message(AdminStates.users_menu, F.text == "🗑️ Видалити користувача")
async def delete_user_start(message: Message, state: FSMContext):
    """Початок процесу видалення користувача"""
    await message.answer(
        "Введіть ID користувача для видалення:",
        reply_markup=get_back_to_admin_kb()
    )
    await state.set_state(AdminStates.deleting_user)

@router.message(AdminStates.deleting_user)
async def delete_user(message: Message, state: FSMContext):
    """Видалення користувача за ID"""
    try:
        user_id = int(message.text)
        
        conn = sqlite3.connect('electronics_store.db')
        cursor = conn.cursor()
        
        # Перевіряємо, чи існує користувач з таким ID
        cursor.execute("SELECT first_name, last_name FROM Customers WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            await message.answer(
                f"❌ Користувача з ID {user_id} не знайдено.",
                reply_markup=get_admin_users_kb()
            )
            await state.set_state(AdminStates.users_menu)
            conn.close()
            return
        
        user_name = f"{user[0]} {user[1]}" if user[1] else user[0]
        
        # Перевіряємо, чи є пов'язані замовлення
        cursor.execute("SELECT COUNT(*) FROM Orders WHERE customer_id = ?", (user_id,))
        orders_count = cursor.fetchone()[0]
        
        if orders_count > 0:
            await message.answer(
                f"⚠️ Користувач '{user_name}' (ID: {user_id}) має {orders_count} замовлень. "
                "Ви впевнені, що хочете видалити користувача та всі його замовлення?",
                reply_markup=get_confirmation_kb()
            )
            await state.update_data(user_id_to_delete=user_id, user_name_to_delete=user_name)
            await state.set_state(AdminStates.confirm_action)
            conn.close()
            return
        
        # Видаляємо користувача
        cursor.execute("DELETE FROM Customers WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        await message.answer(
            f"✅ Користувач '{user_name}' (ID: {user_id}) успішно видалений.",
            reply_markup=get_admin_users_kb()
        )
        await state.set_state(AdminStates.users_menu)
        
    except ValueError:
        await message.answer(
            "❌ Введіть коректний ID користувача (ціле число):",
            reply_markup=get_back_to_admin_kb()
        )
    except Exception as e:
        await message.answer(
            f"❌ Помилка при видаленні користувача: {str(e)}",
            reply_markup=get_admin_users_kb()
        )
        await state.set_state(AdminStates.users_menu)

@router.message(AdminStates.confirm_action, F.text == "✅ Підтвердити")
async def confirm_user_delete(message: Message, state: FSMContext):
    """Підтвердження видалення користувача з замовленнями"""
    data = await state.get_data()
    user_id = data.get("user_id_to_delete")
    user_name = data.get("user_name_to_delete")
    
    try:
        conn = sqlite3.connect('electronics_store.db')
        cursor = conn.cursor()
        
        # Видаляємо замовлення користувача
        cursor.execute("DELETE FROM Orders WHERE customer_id = ?", (user_id,))
        
        # Видаляємо користувача
        cursor.execute("DELETE FROM Customers WHERE id = ?", (user_id,))
        
        conn.commit()
        conn.close()
        
        await message.answer(
            f"✅ Користувач '{user_name}' (ID: {user_id}) та всі його замовлення успішно видалені.",
            reply_markup=get_admin_users_kb()
        )
        await state.set_state(AdminStates.users_menu)
        
    except Exception as e:
        await message.answer(
            f"❌ Помилка при видаленні користувача: {str(e)}",
            reply_markup=get_admin_users_kb()
        )
        await state.set_state(AdminStates.users_menu)

@router.message(AdminStates.confirm_action, F.text == "❌ Скасувати")
async def cancel_user_delete(message: Message, state: FSMContext):
    """Скасування видалення користувача"""
    await message.answer(
        "❌ Видалення користувача скасовано.",
        reply_markup=get_admin_users_kb()
    )
    await state.set_state(AdminStates.users_menu)

# --- УПРАВЛІННЯ ЗАМОВЛЕННЯМИ ---

@router.message(AdminStates.orders_menu, F.text == "📋 Переглянути замовлення")
async def view_orders(message: Message, state: FSMContext):
    """Перегляд всіх замовлень"""
    try:
        conn = sqlite3.connect('electronics_store.db')
        cursor = conn.cursor()
        
        query = """
        SELECT 
            o.id, c.first_name, c.last_name, c.phone_number, 
            p.name, o.quantity, o.total_price, o.order_date, 
            o.delivery_method, o.status 
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.id
        JOIN Products p ON o.product_id = p.id
        ORDER BY o.order_date DESC
        """
        
        cursor.execute(query)
        orders = cursor.fetchall()
        conn.close()
        
        if not orders:
            await message.answer(
                "❌ Замовлень не знайдено.", 
                reply_markup=get_admin_orders_kb()
            )
            return
        
        for order in orders:
            customer_name = f"{order[1]} {order[2]}" if order[2] else order[1]
            phone = order[3] or "Не вказано"
            
            order_info = (
                f"ID замовлення: {order[0]}\n"
                f"Клієнт: {customer_name}\n"
                f"Телефон: {phone}\n"
                f"Товар: {order[4]}\n"
                f"Кількість: {order[5]}\n"
                f"Сума: {order[6]} грн\n"
                f"Дата: {order[7]}\n"
                f"Доставка: {order[8]}\n"
                f"Статус: {order[9]}"
            )
            
            await message.answer(order_info)
            
        await message.answer(
            "✅ Список всіх замовлень відображено.",
            reply_markup=get_admin_orders_kb()
        )
    
    except Exception as e:
        await message.answer(
            f"❌ Помилка: {str(e)}",
            reply_markup=get_admin_orders_kb()
        )

@router.message(AdminStates.orders_menu, F.text == "🔄 Змінити статус замовлення")
async def change_order_status_start(message: Message, state: FSMContext):
    """Початок процесу зміни статусу замовлення"""
    await message.answer(
        "Введіть ID замовлення для зміни статусу:",
        reply_markup=get_back_to_admin_kb()
    )
    await state.set_state(AdminStates.changing_order_status)

@router.message(AdminStates.changing_order_status)
async def select_order_for_status_change(message: Message, state: FSMContext):
    """Вибір замовлення для зміни статусу"""
    try:
        order_id = int(message.text)
        
        conn = sqlite3.connect('electronics_store.db')
        cursor = conn.cursor()
        
        # Перевіряємо, чи існує замовлення з таким ID
        cursor.execute("""
            SELECT o.id, p.name, o.status 
            FROM Orders o
            JOIN Products p ON o.product_id = p.id
            WHERE o.id = ?
        """, (order_id,))
        
        order = cursor.fetchone()
        conn.close()
        
        if not order:
            await message.answer(
                f"❌ Замовлення з ID {order_id} не знайдено.",
                reply_markup=get_admin_orders_kb()
            )
            await state.set_state(AdminStates.orders_menu)
            return
        
        await state.update_data(order_id=order_id, product_name=order[1], current_status=order[2])
        
        await message.answer(
            f"Змінити статус замовлення №{order_id} ({order[1]}).\nПоточний статус: {order[2]}\n\nВиберіть новий статус:",
            reply_markup=get_order_status_kb()
        )
        
    except ValueError:
        await message.answer(
            "❌ Введіть коректний ID замовлення (ціле число):",
            reply_markup=get_back_to_admin_kb()
        )
    except Exception as e:
        await message.answer(
            f"❌ Помилка: {str(e)}",
            reply_markup=get_admin_orders_kb()
        )
        await state.set_state(AdminStates.orders_menu)

@router.message(AdminStates.changing_order_status, F.text.in_(["Pending", "Paid", "Processing", "Shipped", "Delivered", "Cancelled"]))
async def update_order_status(message: Message, state: FSMContext):
    """Оновлення статусу замовлення"""
    data = await state.get_data()
    order_id = data.get("order_id")
    new_status = message.text
    
    try:
        conn = sqlite3.connect('electronics_store.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE Orders SET status = ? WHERE id = ?",
            (new_status, order_id)
        )
        
        conn.commit()
        conn.close()
        
        await message.answer(
            f"✅ Статус замовлення №{order_id} змінено на '{new_status}'.",
            reply_markup=get_admin_orders_kb()
        )
        await state.set_state(AdminStates.orders_menu)
        
    except Exception as e:
        await message.answer(
            f"❌ Помилка при зміні статусу: {str(e)}",
            reply_markup=get_admin_orders_kb()
        )
        await state.set_state(AdminStates.orders_menu)