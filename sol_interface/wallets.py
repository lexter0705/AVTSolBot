from database.workers.wallet import WalletWorker
from sol_interface.wallet_converter import WalletConverter


class Wallets:
    def __init__(self, user_id: int,
                 wallet_converter: WalletConverter,
                 wallet_worker: WalletWorker):
        self.__wallets_database_worker = wallet_worker
        self.__wallet_converter = wallet_converter
        self.__user_id = user_id
        self.__parse_wallets()
        self.__parse_main_wallet()

    def __parse_wallets(self):
        wallets = self.__wallets_database_worker.get_user_not_main_wallets(self.__user_id)
        self.__wallets = []
        for i in wallets:
            self.__wallets.append(self.__wallet_converter.from_private_key(i))

    def __parse_main_wallet(self):
        main_wallet = self.__wallets_database_worker.get_user_main_wallet(self.__user_id)
        self.__main_wallet = self.__wallet_converter.from_private_key(main_wallet)

    def send_from_all_to_main(self):
        pass

    def send_from_main_to_all(self):
        pass

    def buy_token_on_all_wallets(self):
        pass