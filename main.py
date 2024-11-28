import asyncio
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solders.keypair import Keypair
from sqlalchemy.util import await_only

from config import json_checker
from database import WalletWorker, UserWorker
from sol_interface import WalletConverter, TransactionQuoteRequest, TransactionRequest, Wallets
from sol_interface.transaction_sender import AsyncTransactionSender

async def main():
    data = json_checker.get_data()
    worker = WalletWorker(data["database_path"])
    print(worker.select_all())
    print(worker.get_user_main_wallet(0))
    print(worker.get_user_not_main_wallets(0))
    converter = WalletConverter(TransactionQuoteRequest(data["get_quote_link"]),
                                TransactionRequest(data["get_transaction_link"]))
    commintment = Commitment({"maxSupportedTransactionVersion": 0})
    client = AsyncClient("https://api.devnet.solana.com")
    print(await client.is_connected())
    wallets = Wallets(0, converter, worker)
    transaction_sender = AsyncTransactionSender(wallets, client, 10000, "Cz8VBgwj3jJ1C8QZNyzCLvQdiV7X241o5raMkWQVYrBH")
    await transaction_sender.buy_token_on_wallets()

def add_to_db():
    data = json_checker.get_data()
    worker = WalletWorker(data["database_path"])
    # user_worker = UserWorker(data["database_path"])
    # user_worker.insert_new_row({"username": "some_people"})
    # worker.insert_new_row({"user_id": 0,
    #                        "private_key": "UrSkSjcTrAJ3NA4qGnKvLavApTEkCfFotSE9opztgH47pUpJg61QSXvyKH8NZPCvxSfZVvFecnpD9PmQJnisdCj",
    #                        "is_main": True})
    print(worker.select_all())


asyncio.run(main())
