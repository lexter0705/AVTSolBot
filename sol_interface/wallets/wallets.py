from database import WalletWorker
from sol_interface.wallets.wallet import Wallet
from sol_interface.wallets.wallet_converter import WalletConverter


class Wallets:
    def __init__(self, user_id: int,
                 wallet_converter: WalletConverter,
                 wallet_worker: WalletWorker):
        self.__wallets_database_worker = wallet_worker
        self.__wallet_converter = wallet_converter
        self.__user_id = user_id
        self.reload_from_db()

    def __getitem__(self, item) -> Wallet:
        return self.__wallets[item]

    def __len__(self) -> int:
        return len(self.__wallets)

    @property
    def main_wallet(self) -> Wallet:
        return self.__main_wallet

    def __parse_wallets(self):
        wallets = self.__wallets_database_worker.get_user_not_main_wallets(self.__user_id)
        self.__wallets = []
        for i in wallets:
            self.__wallets.append(self.__wallet_converter.from_private_key(i[0]))

    def __parse_main_wallet(self):
        main_wallet = self.__wallets_database_worker.get_user_main_wallet(self.__user_id)
        self.__main_wallet = self.__wallet_converter.from_private_key(main_wallet)

    def reload_from_db(self):
        self.__parse_main_wallet()
        self.__parse_wallets()
