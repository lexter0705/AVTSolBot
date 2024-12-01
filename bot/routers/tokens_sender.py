from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.routers.main_router import solana_worker, bot

router = Router()


@router.callback_query(F.data == "from_all")
async def send_from_all(callback: types.CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Back", callback_data="menu")]])
    solana_worker.add_user(callback.from_user.id)
    sender = solana_worker.get_user_sender(callback.from_user.id)
    message = await bot.send_message(callback.from_user.id, "*Start sending!*", reply_markup=markup)
    try:
        await sender.send_from_all_to_main()
        text = "*Tokens have been sent!*"
    except Exception as e:
        print(e)
        text = "*Error!*"
    await callback.message.delete()
    await message.delete()
    await bot.send_message(callback.from_user.id, text, reply_markup=markup)


@router.callback_query(F.data == "from_main")
async def send_from_main(callback: types.CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Back", callback_data="menu")]])
    solana_worker.add_user(callback.from_user.id)
    sender = solana_worker.get_user_sender(callback.from_user.id)
    message = await bot.send_message(callback.from_user.id, "*Start sending!*", reply_markup=markup)
    try:
        await sender.send_from_main_to_all()
        text = "*Tokens have been sent!*"
    except Exception as e:
        print(e)
        text = "*Error!*"
    await callback.message.delete()
    await message.delete()
    await bot.send_message(callback.from_user.id, text, reply_markup=markup)
