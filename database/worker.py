from typing import Type
from database.creator import Base
from sqlalchemy import create_engine, Executable
from sqlalchemy import insert, select, delete, update


class DatabaseWorker:
    def __init__(self, table: Type[Base], database_path: str):
        database_url = "sqlite:///" + database_path
        engine = create_engine(database_url)
        self.__connect = engine.connect()
        self.__table = table

    def select_all(self):
        data = self.__connect.execute(select(self.__table)).all()
        return data

    def delete_by_id(self, row_id: int):
        request = delete(self.__table).where(self.__table.id == row_id)
        self.commit(request)

    def update_by_id(self, row_id: int, updated_data: dict):
        request = update(self.__table).where(self.__table.id == f"{row_id}").values(**updated_data)
        self.commit(request)

    def insert_new_row(self, data: dict):
        request = insert(self.__table).values(**data)
        self.commit(request)

    def commit(self, request: Executable):
        self.__connect.execute(request)
        self.__connect.commit()

    def get_connect(self):
        return self.__connect