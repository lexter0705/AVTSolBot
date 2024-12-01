from aiogram import types
from solders.keypair import Keypair
from config import json_checker
from database import UserWorker, WalletWorker


class BotDatabase:
    def __init__(self):
        data = json_checker.get_data()
        self.__user_worker = UserWorker(data["database_path"])
        self.__wallet_worker = WalletWorker(data["database_path"])

    @property
    def user_worker(self) -> UserWorker:
        return self.__user_worker

    @property
    def wallet_worker(self) -> WalletWorker:
        return self.__wallet_worker

    def add_user_to_database(self, message: types.Message):
        user = self.__user_worker.get_user(message.from_user.id)
        if not user:
            user_data = {"id": message.from_user.id, "username": message.from_user.username, "period": 15}
            self.__user_worker.insert_new_row(user_data)
            wallet_data = {"user_id": message.from_user.id, "private_key": str(Keypair()), "is_main": True}
            self.__wallet_worker.insert_new_row(wallet_data)

    def add_new_wallets_to_database(self, message: types.Message, count: int):
        for i in range(count):
            wallet_data = {"user_id": message.from_user.id, "private_key": str(Keypair()), "is_main": False}
            self.__wallet_worker.insert_new_row(wallet_data)