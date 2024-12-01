from sqlalchemy import select, update

from database.creator import UserTable
from database.worker import DatabaseWorker


class UserWorker(DatabaseWorker):
    def __init__(self, database_path: str):
        super().__init__(UserTable, database_path)

    def get_user(self, user_id: int):
        users = self.connect.execute(select(UserTable).where(UserTable.id == user_id)).first()
        return users

    def set_period(self, user_id: int, new_period: int):
        request = update(UserTable).where(UserTable.id == f"{user_id}").values(period=new_period)
        self.commit(request)