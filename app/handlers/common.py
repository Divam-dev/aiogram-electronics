from aiogram.fsm.state import State, StatesGroup

class OrderStates(StatesGroup):
    choosing_currency = State()
    choosing_category = State()
    viewing_products = State()
    viewing_cart = State()
    choosing_delivery = State()
    entering_phone = State()
    entering_email = State()
    confirming_payment = State()

carts = {}