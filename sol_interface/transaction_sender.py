from solana.rpc.async_api import AsyncClient

from sol_interface import Wallets


class AsyncTransactionSender:
    def __init__(self, wallets: Wallets, client: AsyncClient,
                 token: str, additional_fee: int = 0):
        self.__wallets = wallets
        self.__client = client
        self.__additional_fee = additional_fee
        self.__token = token

    @property
    def wallets(self) -> Wallets:
        return self.__wallets

    async def send_from_all_to_main(self):
        for wallet in self.__wallets:
            count = (await self.__client.get_balance(wallet.public_key)).value
            message = wallet.send_sol(self.__wallets.main_wallet.public_key, count,
                                      (await self.__client.get_latest_blockhash()).value.blockhash)
            fee = await self.__client.get_fee_for_message(message.message)
            count -= fee.value + self.__additional_fee
            if count <= 0:
                continue
            message = wallet.send_sol(self.__wallets.main_wallet.public_key, count,
                                      (await self.__client.get_latest_blockhash()).value.blockhash)
            await self.__client.send_transaction(message)

    async def send_from_main_to_all(self):
        all_count = (await self.__client.get_balance(self.__wallets.main_wallet.public_key)).value
        count_to_send = all_count / len(self.__wallets)
        count_to_send = round(count_to_send)
        for wallet in self.__wallets:
            message = self.__wallets.main_wallet.send_sol(wallet.public_key, count_to_send,
                                                          (await self.__client.get_latest_blockhash()).value.blockhash)
            fee = await self.__client.get_fee_for_message(message.message)
            count = count_to_send - fee.value - self.__additional_fee
            if count <= 0:
                continue
            message = self.__wallets.main_wallet.send_sol(wallet.public_key, count,
                                                          (await self.__client.get_latest_blockhash()).value.blockhash)
            await self.__client.send_transaction(message)

    async def buy_token_on_wallets(self):
        for wallet in self.__wallets:
            message = wallet.buy_token(self.__token, 3000000, 100)
            await self.__client.send_transaction(message)

    def reload_wallets(self):
        self.__wallets.reload_from_db()
