import os
from PySide6 import QtSql
from typing import Any


class Database:
    def __init__(self) -> None:
        self.db = QtSql.QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName(os.environ["DB_HOSTNAME"])
        self.db.setPort(int(os.environ["DB_PORT"]))
        self.db.setDatabaseName(os.environ["DB_NAME"])
        self.db.setUserName(os.environ["DB_USERNAME"])
        self.db.setPassword(os.environ["DB_PASSWORD"])
        ok = self.db.open()
        if not ok:
            raise ConnectionError

    def _check(self, func, *args):
        if not func(*args):
            raise ValueError(func.__self__.lastError())

    def get_tables(self) -> list[str]:
        query = QtSql.QSqlQuery("""
            select table_name from information_schema.tables
            where table_schema='public' and table_type='BASE TABLE';
            """, db=self.db)
        table_name_field = query.record().indexOf("table_name")
        result = []
        while query.next():
            result.append(query.value(table_name_field))
        return result

    def get_entries(self, table: str) -> list[list[Any]]:
        query = QtSql.QSqlQuery(f"select * from {table}", db=self.db)
        result = []
        while query.next():
            result.append([query.value(index) for index in range(query.record().count())])
        return result

    def get_columns(self, table: str) -> list[str]:
        query = QtSql.QSqlQuery(f"select * from {table}", db=self.db)
        record = query.record()
        return [record.fieldName(id) for id in range(record.count())]

    def create_entry(self, table: str, values: dict[str, Any]) -> None:
        query = QtSql.QSqlQuery(db=self.db)
        new = ','.join([f"'{value}'" for value in values.values()])
        query.prepare(f"insert into {table} ({','.join(values.keys())}) values ({new})")
        self._check(query.exec)

    def update_entry(self, table: str, old_values: dict[str, Any], new_values: dict[str, Any]) -> None:
        query = QtSql.QSqlQuery(db=self.db)
        new = ','.join([f"{key}='{new_values[key]}'" for key in new_values.keys()])
        old = ','.join([f"{key}='{old_values[key]}'" for key in old_values.keys()])
        query.prepare(f"update {table} set {new} where {old}")
        self._check(query.exec)

    def delete_entry(self, table: str, values: dict[str, Any]) -> None:
        query = QtSql.QSqlQuery(db=self.db)
        condition = ','.join([f"{key}='{values[key]}'" for key in values.keys()])
        query.prepare(f"delete from {table} where {condition}")
        self._check(query.exec)

