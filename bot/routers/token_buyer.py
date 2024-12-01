from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.formatting import Text

from bot.modules.token_buyer import TokenBuyer
from bot.routers.main_router import solana_worker, bot, database

router = Router()
buyer = TokenBuyer(solana_worker, database)


@router.callback_query(F.data == "buy")
async def start_buy_loop(callback: types.CallbackQuery):
    keyboard = [[InlineKeyboardButton(text="Back", callback_data="menu")],
                [InlineKeyboardButton(text="Stop buy", callback_data="stop")],
                [InlineKeyboardButton(text="Set pause time", callback_data="pause")]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    solana_worker.add_user(callback.from_user.id)
    if not buyer.is_in_loop(callback.from_user.id):
        text = "*Bot start buy tokens!*"
        await callback.message.delete()
        await bot.send_message(callback.from_user.id, text, reply_markup=markup)
        await buyer.start_buy_loop(callback.from_user.id)
    else:
        text = "*Bot every buying tokens*"
        await callback.message.delete()
        await bot.send_message(callback.from_user.id, text, reply_markup=markup)


@router.callback_query(F.data == "stop")
async def stop_buy_loop(callback: types.CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Back", callback_data="menu")]])
    solana_worker.add_user(callback.from_user.id)
    await buyer.stop_loop(callback.from_user.id)
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, "*Buying was stop*", reply_markup=markup)


@router.callback_query(F.data == "pause")
async def set_pause_period(callback: types.CallbackQuery):
    keyboard = [
        [InlineKeyboardButton(text="15", callback_data="time_15"),
         InlineKeyboardButton(text="10", callback_data="time_10")],
        [InlineKeyboardButton(text="60", callback_data="time_60"),
         InlineKeyboardButton(text="30", callback_data="time_30")]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, "*Select the inspection period*", reply_markup=markup)


@router.callback_query(F.data.startswith("time_"))
async def set_time(callback: types.CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Back", callback_data="buy")]])
    number = int(callback.data.split("_")[1])
    database.user_worker.set_period(callback.from_user.id, number)
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, "*Period was set*", reply_markup=markup)
