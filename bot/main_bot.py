from aiogram import Bot, Dispatcher, executor, types
from bot.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Привет! Я Avito_parser_new_bot. Напиши /search чтобы найти объявления.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)