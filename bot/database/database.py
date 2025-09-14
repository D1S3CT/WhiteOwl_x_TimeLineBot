"""
Модуль подключения к базе данных PostgreSQL.
"""

import asyncpg
from config.settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


class Database:
    """
    Класс для работы с базой данных PostgreSQL.
    """

    def __init__(self):
        """
        Инициализирует параметры подключения к базе данных.
        """
        self.host = DB_HOST
        self.port = DB_PORT
        self.database = DB_NAME
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.pool = None

    async def connect(self) -> None:
        """
        Создает пул соединений с базой данных.

        Raises:
            Exception: Если не удалось подключиться к базе данных
        """
        try:
            self.pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                min_size=1,
                max_size=10
            )
            print("Подключение к базе данных успешно установлено")
        except Exception as e:
            raise Exception(f"Не удалось подключиться к базе данных: {e}")

    async def disconnect(self) -> None:
        """
        Закрывает пул соединений с базой данных.
        """
        if self.pool:
            await self.pool.close()
            print("Подключение к базе данных закрыто")

    async def execute(self, query: str, *args) -> None:
        """
        Выполняет SQL-запрос без возврата результата.

        Args:
            query (str): SQL-запрос
            *args: Параметры для запроса

        Raises:
            Exception: Если произошла ошибка при выполнении запроса
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query, *args)

    async def fetch(self, query: str, *args) -> list:
        """
        Выполняет SQL-запрос и возвращает список результатов.

        Args:
            query (str): SQL-запрос
            *args: Параметры для запроса

        Returns:
            list: Список результатов запроса

        Raises:
            Exception: Если произошла ошибка при выполнении запроса
        """
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        """
        Выполняет SQL-запрос и возвращает одну строку результата.

        Args:
            query (str): SQL-запрос
            *args: Параметры для запроса

        Returns:
            Row: Одна строка результата или None

        Raises:
            Exception: Если произошла ошибка при выполнении запроса
        """
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)