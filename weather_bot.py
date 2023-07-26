import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from dotenv import load_dotenv

# Set up the Telegram bot


load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher(bot)

# Set up the OpenWeatherMap API
OWM_API_KEY = os.getenv("OWM_API_KEY")

OWM_API_URL = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric'

# Handle the /start command
@dp.message_handler(commands=['weather'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm Weather Bot. Please send me the name of a city and I'll tell you the weather there.")

# Handle text messages
@dp.message_handler()
async def send_weather(message: types.Message):
    city_name = message.text
    api_url = OWM_API_URL.format(city=city_name, key=OWM_API_KEY)
    response = requests.get(api_url)
    
    if response.status_code == 200:
        weather_data = response.json()
        weather_info = f"Current weather in {city_name}: {weather_data['weather'][0]['description']}. Temperature: {weather_data['main']['temp']} °C"
        await message.reply(weather_info)
    else:
        await message.reply(f"Sorry, I could not retrieve weather data for {city_name}. Please try again.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)