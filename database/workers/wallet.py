from sqlalchemy import select
from database.creator import WalletTable
from database.worker import DatabaseWorker


class WalletWorker(DatabaseWorker):
    def __init__(self):
        super().__init__(WalletTable)

    def get_user_not_main_wallets(self, user_id: int) -> list[str]:
        request = select(WalletTable).where(WalletTable.user_id == user_id)
        return self.get_connect().execute(request).all()

    def get_user_main_wallet(self, user_id: int) -> str:
        request = select(WalletTable).where(WalletTable.user_id == user_id and WalletTable.is_main)
        return self.get_connect().execute(request).first()