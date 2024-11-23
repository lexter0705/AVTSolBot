from database.creator import User
from database.worker import DatabaseWorker


class UserWorker(DatabaseWorker):
    def __init__(self):
        super().__init__(User)