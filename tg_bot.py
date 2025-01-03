import asyncio
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.filters.command import Command
import random
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode  # Исправлено имя класса
from credentials import BOT_KEY

API_TOKEN = BOT_KEY

# Создаем объект Bot
bot = Bot(token=API_TOKEN, defaults=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Сообщение с <u>HTML-разметкой</u>")  # HTML разметка
    parse_mode=ParseMode.HTML

# Обработчик команды /finish
@dp.message(Command("finish"))
async def finish_command(message: types.Message):
    await message.answer(f"{random.randint(1, 10)}")  # Генерация случайного числа

# Основная функция запуска
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
