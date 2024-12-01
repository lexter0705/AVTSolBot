from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.routers.main_router import database, bot

router = Router()


class Form(StatesGroup):
    count = State()


@router.callback_query(F.data == "create_new_children")
async def to_children(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.count)
    await bot.send_message(callback.from_user.id, "Input count wallets:")


@router.message(Form.count)
async def get_count(message: types.Message, state: FSMContext):
    await state.set_state()
    try:
        count = int(message.text)
        database.add_new_wallets_to_database(message, count)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="To menu", callback_data="menu")]])
        await bot.send_message(message.from_user.id, "Created!", reply_markup=keyboard)
    except ValueError:
        await message.reply("Please enter an integer.")
