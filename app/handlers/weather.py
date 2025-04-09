import requests
import logging
import os
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove

class WeatherStates(StatesGroup):
    waiting_for_city = State()

router = Router()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5"

weather_emojis = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Haze": "🌫️",
    "Smoke": "🌫️",
    "Dust": "🌫️",
    "Sand": "🌫️",
    "Ash": "🌫️",
    "Squall": "💨",
    "Tornado": "🌪️"
}

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius"""
    return round(kelvin - 273.15, 1)

def get_weather_emoji(weather_main):
    """Get weather emoji based on condition"""
    return weather_emojis.get(weather_main, "🌡️")

async def get_current_weather(city):
    """Get current weather for a city"""
    try:
        response = requests.get(
            f"{WEATHER_API_URL}/weather",
            params={
                "q": city,
                "appid": WEATHER_API_KEY,
                "lang": "ua"
            }
        )
        data = response.json()
        
        if response.status_code != 200:
            return f"❌ Помилка: {data.get('message', 'Місто не знайдено')}"
        
        temp = kelvin_to_celsius(data["main"]["temp"])
        feels_like = kelvin_to_celsius(data["main"]["feels_like"])
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        weather_main = data["weather"][0]["main"]
        weather_description = data["weather"][0]["description"]
        
        weather_emoji = get_weather_emoji(weather_main)
        
        return (
            f"🏙️ Погода в місті {city}:\n\n"
            f"{weather_emoji} {weather_description.capitalize()}\n"
            f"🌡️ Температура: {temp}°C (відчувається як {feels_like}°C)\n"
            f"💧 Вологість: {humidity}%\n"
            f"💨 Швидкість вітру: {wind_speed} м/с"
        )
    
    except Exception as e:
        logging.error(f"Error fetching current weather: {e}")
        return "❌ Помилка при отриманні даних про погоду. Спробуйте пізніше."

async def get_weather_forecast(city):
    """Get 5-day weather forecast for a city"""
    try:
        response = requests.get(
            f"{WEATHER_API_URL}/forecast",
            params={
                "q": city,
                "appid": WEATHER_API_KEY,
                "lang": "uk"
            }
        )
        data = response.json()
        
        if response.status_code != 200:
            return f"❌ Помилка: {data.get('message', 'Місто не знайдено')}"
        
        forecasts = []
        processed_dates = set()
        
        for item in data["list"]:
            date = item["dt_txt"].split(" ")[0]
            time = item["dt_txt"].split(" ")[1]
            
            if date in processed_dates or not ("12:00:00" in time or "15:00:00" in time):
                continue
            
            processed_dates.add(date)
            
            temp = kelvin_to_celsius(item["main"]["temp"])
            weather_main = item["weather"][0]["main"]
            weather_description = item["weather"][0]["description"]
            weather_emoji = get_weather_emoji(weather_main)
            
            day, month = date.split("-")[2], date.split("-")[1]
            formatted_date = f"{day}.{month}"
            
            forecasts.append(
                f"{formatted_date}: {weather_emoji} {temp}°C, {weather_description}"
            )
            
            if len(forecasts) >= 3:
                break
        
        if not forecasts:
            return "❌ Не вдалося отримати прогноз погоди."
        
        forecast_text = "\n".join(forecasts)
        return f"📅 Прогноз погоди на наступні дні для {city}:\n\n{forecast_text}"
    
    except Exception as e:
        logging.error(f"Error fetching weather forecast: {e}")
        return "❌ Помилка при отриманні прогнозу погоди. Спробуйте пізніше."

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