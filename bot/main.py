import asyncio
from aiogram import Dispatcher
from router import router, bot

dp = Dispatcher()
dp.include_router(router)


async def run():
    await dp.start_polling(bot)


asyncio.run(run())
