from solana.rpc.async_api import AsyncClient

from config import json_checker
from database import WalletWorker
from sol_interface import TransactionQuoteRequest, TransactionRequest, WalletConverter, AsyncTransactionSender, Wallets
from sol_interface.requests.buy import TokensBuyRequest


class SolanaWorker:
    def __init__(self):
        data = json_checker.get_data()
        self.__user_senders: dict[int, AsyncTransactionSender] = {}
        self.__client = AsyncClient(data["rpc_url"])
        self.__wallet_converter = WalletConverter(TransactionQuoteRequest(data["get_quote_link"]),
                                                  TransactionRequest(data["get_transaction_link"]),
                                                  TokensBuyRequest(data["rpc_url"], data["get_buy_link"]))
        self.__wallet_worker = WalletWorker(data["database_path"])
        self.__token = data["token_for_buy"]

    @property
    def client(self) -> AsyncClient:
        return self.__client

    def add_user(self, user_id: int):
        if user_id in self.__user_senders.keys():
            return

        wallets = Wallets(user_id, self.__wallet_converter, self.__wallet_worker)
        self.__user_senders[user_id] = AsyncTransactionSender(wallets, self.__client, self.__token, 3_000_000)

    def get_user_sender(self, user_id: int) -> AsyncTransactionSender:
        return self.__user_senders[user_id]

    def reload_wallets(self, user_id: int):
        self.__user_senders[user_id].reload_wallets()

    async def get_user_balance(self, user_id: int) -> int:
        pubkey = self.__user_senders[user_id].wallets.main_wallet.public_key
        return (await self.__client.get_balance(pubkey)).value