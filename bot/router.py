from aiogram import Router, types, F, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.modules.main_database import BotDatabase
from bot.modules.solana_worker import SolanaWorker
from bot.modules.strings_former import StringsFormer

bot = Bot(token='7004388668:AAEEfvIXpuNwNemcJlt1TaEEZOzD7rwX4tQ',
          default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
router = Router()
database = BotDatabase()
solana_worker = SolanaWorker()
strings_former = StringsFormer(solana_worker.client)


@router.message(CommandStart())
async def start(message: types.Message):
    database.add_user_to_database(message)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="To menu", callback_data="menu")]])
    await message.reply("Hello! I am bot for buy CBDAI token.", reply_markup=keyboard)


@router.callback_query(F.data == "menu")
async def to_menu(callback: types.CallbackQuery):
    buttons = [[InlineKeyboardButton(text="To children", callback_data="children")]]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    wallet = solana_worker.get_user_sender(callback.from_user.id).wallets.main_wallet
    text = await strings_former.form_string(wallet)
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, text, reply_markup=markup)


@router.callback_query(F.data == "children")
async def to_children(callback: types.CallbackQuery):
    buttons = [[InlineKeyboardButton(text="Create new children", callback_data="create_new_children")],
               [InlineKeyboardButton(text="Back", callback_data="menu")]]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    children = solana_worker.get_user_sender(callback.from_user.id).wallets
    text = "*You not have other wallets*"
    if len(children) > 0:
        text = await strings_former.form_string(children)
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, text, reply_markup=markup)


@router.callback_query(F.data == "create_new_children")
async def to_children(callback: types.CallbackQuery):
    pass
