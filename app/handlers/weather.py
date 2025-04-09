from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove

from app.services.weather_service import get_current_weather, get_weather_forecast

class WeatherStates(StatesGroup):
    waiting_for_city = State()

router = Router()

@router.message(Command("weather"))
async def weather_command(message: Message, state: FSMContext):
    """Handle /weather command"""
    await state.set_state(WeatherStates.waiting_for_city)
    await message.answer(
        "🌤️ Введіть назву міста для отримання прогнозу погоди:",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(WeatherStates.waiting_for_city)
async def process_city(message: Message, state: FSMContext):
    city = message.text.strip()
    
    await message.bot.send_chat_action(message.chat.id, 'typing')
    
    current_weather = await get_current_weather(city)
    await message.answer(current_weather)
    
    if not current_weather.startswith("❌"):
        forecast = await get_weather_forecast(city)
        await message.answer(forecast)
        
        await state.set_state(None)
    else:
        await message.answer("Спробуйте ввести інше місто")