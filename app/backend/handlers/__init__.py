from typing import Any


def get_tables() -> list[str]:
    """возвращает названия всех табличек в бд"""
    return ["t1", "t2"]


def get_entries(table: str) -> list[list[Any]]:
    """возвращает все записи в таблице table"""
    return [[1, "name1"], [2, "name2"]]


def get_columns(table: str) -> list[str]:
    """возвращает названия всех столбцов в таблице table"""
    return ["id", "name"]


def create_entry(table: str, old_kwargs: dict[str, Any], new_kwargs: dict[str, Any]) -> None:
    """обновляет запись с ключами-значениями old_kwargs на new_kwargs в таблице table.
    Значения при одинаковых ключах в old_kwargs и new_kwargs чаще всего будут совпадать"""


def delete_entry(table: str, kwargs: dict) -> None:
    """удаляет запись с ключами-значениями kwargs из таблицы table"""
