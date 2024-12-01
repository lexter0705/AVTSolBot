import asyncio
from aiogram import Dispatcher
from bot.routers.main_router import router, bot
from bot.routers.new_account_creator import router as new_account_creator
from bot.routers.tokens_sender import router as token_sender
from bot.routers.token_buyer import router as token_buyer

dp = Dispatcher()
dp.include_router(router)
dp.include_router(new_account_creator)
dp.include_router(token_sender)
dp.include_router(token_buyer)


async def run():
    await dp.start_polling(bot)


asyncio.run(run())
