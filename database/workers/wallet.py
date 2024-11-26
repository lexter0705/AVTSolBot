from database.creator import WalletTable
from database.worker import DatabaseWorker


class WalletWorker(DatabaseWorker):
    def __init__(self):
        super().__init__(WalletTable)

    def get_user_not_main_wallets(self, user_id: int) -> list[str]:
        pass

    def get_user_main_wallet(self, user_id: int) -> str:
        pass