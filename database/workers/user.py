from database.creator import UserTable
from database.worker import DatabaseWorker


class UserWorker(DatabaseWorker):
    def __init__(self, database_path: str):
        super().__init__(UserTable, database_path)