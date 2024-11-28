from sqlalchemy import select, and_
from database.creator import WalletTable
from database.worker import DatabaseWorker


class WalletWorker(DatabaseWorker):
    def __init__(self, database_path: str):
        super().__init__(WalletTable, database_path)

    def get_user_not_main_wallets(self, user_id: int) -> list[str]:
        request = select(WalletTable.private_key).where(and_(WalletTable.user_id == user_id, WalletTable.is_main != True))
        return self.connect.execute(request).all()

    def get_user_main_wallet(self, user_id: int) -> str:
        request = select(WalletTable.private_key).where(and_(WalletTable.user_id == user_id, WalletTable.is_main))
        return self.connect.execute(request).first()[0]