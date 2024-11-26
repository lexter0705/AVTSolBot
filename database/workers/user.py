from database.creator import UserTable
from database.worker import DatabaseWorker


class UserWorker(DatabaseWorker):
    def __init__(self):
        super().__init__(UserTable)