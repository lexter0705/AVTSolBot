import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from commands import router

dp = Dispatcher()
dp.include_router(router)


async def main():
    bot = Bot(token='7004388668:AAEEfvIXpuNwNemcJlt1TaEEZOzD7rwX4tQ', default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    await dp.start_polling(bot)

asyncio.run(main())