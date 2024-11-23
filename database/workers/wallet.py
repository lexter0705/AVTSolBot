from database.creator import Wallet
from database.worker import DatabaseWorker


class WalletWorker(DatabaseWorker):
    def __init__(self):
        super().__init__(Wallet)

    def get_user_wallets(self):
        pass