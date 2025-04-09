from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums import ContentType

from app.keyboards import get_menu_kb, get_delivery_method_kb
from app.handlers.common import OrderStates, carts
from app.handlers.cart import view_cart
from app.payment import create_redsys_invoice

router = Router()

@router.message(OrderStates.choosing_delivery, F.text == "🏪 Самовивіз")
async def process_self_pickup(message: Message, state: FSMContext):
    await state.update_data(delivery_method="self_pickup")
    
    # Для самовивозу нам все ще потрібен номер телефону
    await state.set_state(OrderStates.entering_phone)
    await message.answer(
        "Ви обрали самовивіз. Для оформлення замовлення, будь ласка, введіть ваш номер телефону у форматі +380XXXXXXXXX:",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(OrderStates.choosing_delivery, F.text == "🚚 Оплатити зараз")
async def process_immediate_payment(message: Message, state: FSMContext):
    """Обробка вибору оплати через Redsys - відразу переходимо до платіжної форми"""
    chat_id = message.chat.id
    
    if not carts.get(chat_id):
        await message.answer("Помилка: кошик порожній")
        return
        
    await state.update_data(delivery_method="immediate_payment")
    
    try:
        # Створюємо дані користувача для платіжної системи
        # Тут не потрібні телефон та email, оскільки їх збере платіжна форма
        user_data = {
            "chat_id": chat_id,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "currency_code": (await state.get_data()).get("currency_code", "UAH")
        }
        
        # Отримуємо дані для оплати Redsys
        payment_data = create_redsys_invoice(carts[chat_id], user_data)
        
        if payment_data.get("reason") == "Ok":
            # Зберігаємо посилання на замовлення
            await state.update_data(order_reference=payment_data.get("orderReference"))
            
            # Надсилаємо платіжну форму користувачу
            invoice_data = payment_data.get("invoice_data")
            
            await message.bot.send_invoice(
                chat_id=chat_id,
                title=invoice_data["title"],
                description=invoice_data["description"],
                payload=invoice_data["payload"],
                provider_token=invoice_data["provider_token"],
                currency=invoice_data["currency"],
                prices=invoice_data["prices"],
                need_name=invoice_data["need_name"],
                need_phone_number=invoice_data["need_phone_number"],
                need_email=invoice_data["need_email"]
            )
            
            await message.answer(
                "✅ Будь ласка, заповніть платіжну форму для завершення замовлення.",
                reply_markup=get_menu_kb()
            )
            
            await state.set_state(OrderStates.confirming_payment)
            
        else:
            await message.answer(
                f"❌ Помилка при створенні платежу: {payment_data.get('reason', 'Невідома помилка')}.\n"
                "Спробуйте ще раз або зв'яжіться з нами для допомоги.",
                reply_markup=get_menu_kb()
            )
            await state.set_state(OrderStates.choosing_category)
            
    except Exception as e:
        await message.answer(
            f"❌ Виникла помилка при обробці платежу: {str(e)}.\n"
            "Будь ласка, спробуйте ще раз пізніше або зв'яжіться з нами для допомоги.",
            reply_markup=get_menu_kb()
        )
        await state.set_state(OrderStates.choosing_category)

@router.message(OrderStates.choosing_delivery, F.text == "🔙 Назад до кошику")
async def back_to_cart(message: Message, state: FSMContext):
    await view_cart(message, state)

@router.message(OrderStates.entering_phone)
async def process_phone_number(message: Message, state: FSMContext):
    chat_id = message.chat.id
    phone_number = message.text
    
    # Базова перевірка телефону
    if not (phone_number.startswith("+380") and len(phone_number) == 13 and phone_number[1:].isdigit()):
        await message.answer("Будь ласка, введіть коректний номер телефону у форматі +380XXXXXXXXX")
        return
    
    await state.update_data(phone=phone_number)
    
    # Для самовивозу не потрібна email, переходимо відразу до підтвердження
    data = await state.get_data()
    if data.get("delivery_method") == "self_pickup":
        await process_self_pickup_confirmation(message, state)
    else:
        await state.set_state(OrderStates.entering_email)
        await message.answer("Введіть ваш email для отримання квитанції:")

@router.message(OrderStates.entering_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text
    
    # Базова перевірка email
    if "@" not in email or "." not in email:
        await message.answer("Будь ласка, введіть коректний email")
        return
    
    await state.update_data(email=email)
    await process_self_pickup_confirmation(message, state)

async def process_self_pickup_confirmation(message: Message, state: FSMContext):
    chat_id = message.chat.id
    data = await state.get_data()
    
    await message.answer(
        "✅ Ваше замовлення на самовивіз успішно оформлено!\n\n"
        f"Наш менеджер зв'яжеться з вами за номером {data.get('phone')} "
        "для підтвердження деталей замовлення та адреси самовивозу.\n\n"
        "Дякуємо за замовлення!",
        reply_markup=get_menu_kb()
    )
    
    if chat_id in carts:
        carts[chat_id] = {}
    
    await state.set_state(OrderStates.choosing_category)

# Handle pre-checkout queries
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query, bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Handle successful payments
@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message, state: FSMContext):
    # Зберігаємо контактні дані з платіжної форми для можливого використання
    payment_info = message.successful_payment
    
    # Очищаємо кошик користувача
    chat_id = message.chat.id
    if chat_id in carts:
        carts[chat_id] = {}
    
    await message.answer(
        "✅ Дякуємо за оплату! Ваше замовлення успішно оформлено.\n"
        "Наш менеджер зв'яжеться з вами найближчим часом для уточнення деталей доставки.",
        reply_markup=get_menu_kb()
    )
    
    await state.set_state(OrderStates.choosing_category)

# Обробник для підтвердження оплати
@router.message(OrderStates.confirming_payment)
async def check_payment_status(message: Message, state: FSMContext):
    if message.text.lower() in ["назад", "скасувати", "відмінити", "cancel"]:
        await message.answer("Ви скасували оплату і повертаєтесь до меню.", reply_markup=get_menu_kb())
        await state.set_state(OrderStates.choosing_category)
        return
    
    await message.answer(
        "Щоб оплатити замовлення, будь ласка, використайте платіжну форму, яку ми вам надіслали.\n"
        "Якщо у вас виникли проблеми з оплатою, спробуйте ще раз або зв'яжіться з нами для допомоги.",
        reply_markup=get_menu_kb()
    )