from database.workers.wallet import WalletWorker
from sol_interface.wallet_converter import WalletConverter
from solders.bankrun import BanksClient


class Wallets:
    def __init__(self, user_id: int,
                 wallet_converter: WalletConverter,
                 wallet_worker: WalletWorker,
                 client: BanksClient,
                 token_for_buy_hex: str):
        self.__wallets_database_worker = wallet_worker
        self.__wallet_converter = wallet_converter
        self.__user_id = user_id
        self.__client = client
        self.__parse_wallets()
        self.__parse_main_wallet()
        self.__token = token_for_buy_hex

    def __parse_wallets(self):
        wallets = self.__wallets_database_worker.get_user_not_main_wallets(self.__user_id)
        self.__wallets = []
        for i in wallets:
            self.__wallets.append(self.__wallet_converter.from_private_key(i))

    def __parse_main_wallet(self):
        main_wallet = self.__wallets_database_worker.get_user_main_wallet(self.__user_id)
        self.__main_wallet = self.__wallet_converter.from_private_key(main_wallet)

    async def send_from_all_to_main(self):
        for wallet in self.__wallets:
            count = await self.__client.get_balance(wallet.get_pubkey())
            message = wallet.send_sol(self.__main_wallet.get_pubkey(), count)
            await self.__client.send_transaction(message)

    async def send_from_main_to_all(self):
        all_count = await self.__client.get_balance(self.__main_wallet.get_pubkey())
        count_to_send = all_count / len(self.__wallets)
        for wallet in self.__wallets:
            message = self.__main_wallet.send_sol(wallet.get_pubkey(), count_to_send)
            await self.__client.send_transaction(message)

    async def buy_token_on_all_wallets(self):
        for wallet in self.__wallets:
            message = wallet.buy_token(self.__token, await self.__client.get_balance(wallet.get_pubkey()))
            await self.__client.send_transaction(message)