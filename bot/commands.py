from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair

from config import json_checker
from database import UserWorker, WalletWorker
from sol_interface import Wallets, WalletConverter
from sol_interface.requests.quote import TransactionQuoteRequest
from sol_interface.requests.transaction import TransactionRequest
from sol_interface.transaction_sender import AsyncTransactionSender

router = Router()

data = json_checker.get_data()
user_worker = UserWorker(data["database_path"])
wallet_worker = WalletWorker(data["database_path"])
converter = WalletConverter(TransactionQuoteRequest(data["get_quote_link"]),
                            TransactionRequest(data["get_transaction_link"]))
client = AsyncClient("https://api.mainnet-beta.solana.com")
wallets = Wallets(0, converter, wallet_worker)
transaction_sender = AsyncTransactionSender(wallets, client, 10000, "Cz8VBgwj3jJ1C8QZNyzCLvQdiV7X241o5raMkWQVYrBH")


@router.message(CommandStart())
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="To menu", callback_data="menu")]])
    await message.reply("Hello! I am bot for buy CBDAI token.", reply_markup=keyboard)


@router.callback_query(F.data == "menu")
async def to_menu(callback: types.CallbackQuery):
    user = user_worker.get_user(callback.message.from_user.id)
    if not user:
        user_worker.insert_new_row(
            {"id": callback.message.from_user.id, "username": callback.message.from_user.username})
        wallet_worker.insert_new_row(
            {"user_id": callback.message.from_user.id, "private_key": str(Keypair()), "is_main": True})
    user_private_key = wallet_worker.get_user_main_wallet(callback.message.from_user.id)
    keypair = Keypair.from_base58_string(user_private_key)
    user_public_key = keypair.pubkey()
    await callback.message.edit_text(
        f"*Your main account:*\n{user_public_key}\n*Balance:* {(await client.get_balance(user_public_key)).value}")
    await callback.message.edit_reply_markup(
        inline_keyboard=[[InlineKeyboardButton(text="To children", callback_data="children")]])


@router.callback_query(F.data == "children")
async def to_children(callback: types.CallbackQuery):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Create new children", callback_data="create_new_children")],
                         [InlineKeyboardButton(text="Back", callback_data="menu")]])
    children = wallet_worker.get_user_not_main_wallets(callback.message.from_user.id)
    await callback.message.edit_text(await form_account_data(children))
    await callback.message.edit_reply_markup(reply_markup=markup)


async def form_account_data(private_keys: list[str]) -> str:
    returned = ""
    for i in private_keys:
        keypair = Keypair.from_base58_string(i)
        public_key = keypair.pubkey()
        count = (await client.get_balance(public_key)).value
        returned += f"*Your main account:*\n{public_key}\n*Balance:* {count}\n"
    return returned
