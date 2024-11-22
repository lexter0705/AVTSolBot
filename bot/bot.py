from aiogram import Bot, Dispatcher
from commands import router

dp = Dispatcher()
dp.include_router(router)


async def main():
    bot = Bot(token='7004388668:AAEEfvIXpuNwNemcJlt1TaEEZOzD7rwX4tQ')
    await dp.start_polling(bot)