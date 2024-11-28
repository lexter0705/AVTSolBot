from solana.rpc.async_api import AsyncClient
from sol_interface import Wallets


class AsyncTransactionSender:
    def __init__(self, wallets: Wallets, client: AsyncClient,
                 fee: int, token: str):
        self.__wallets = wallets
        self.__client = client
        self.__fee = fee
        self.__token = token

    async def send_from_all_to_main(self):
        for wallet in self.__wallets:
            count = (await self.__client.get_balance(wallet.public_key)).value
            message = wallet.send_sol(self.__wallets.main_wallet.public_key, count,
                                      (await self.__client.get_latest_blockhash()).value.blockhash)
            await self.__client.send_transaction(message)

    async def send_from_main_to_all(self):
        all_count = (await self.__client.get_balance(self.__wallets.main_wallet.public_key)).value
        count_to_send = (all_count - (self.__fee * len(self.__wallets))) / len(self.__wallets)
        count_to_send = round(count_to_send)
        for wallet in self.__wallets:
            message = self.__wallets.main_wallet.send_sol(wallet.public_key, count_to_send,
                                                          (await self.__client.get_latest_blockhash()).value.blockhash)
            await self.__client.send_transaction(message)

    async def buy_token_on_wallets(self):
        for wallet in self.__wallets:
            message = wallet.buy_token(self.__token, 3000000,100)
            await self.__client.send_transaction(message)
