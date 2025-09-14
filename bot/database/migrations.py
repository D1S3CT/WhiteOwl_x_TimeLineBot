"""
Модуль управления миграциями базы данных.
"""

import os
import asyncio
from bot.database.database import Database


class MigrationManager:
    """
    Класс для управления миграциями базы данных.
    """

    def __init__(self, database: Database, migrations_dir: str = "migrations"):
        """
        Инициализирует менеджер миграций.

        Args:
            database (Database): Объект подключения к базе данных
            migrations_dir (str): Директория с файлами миграций
        """
        self.database = database
        self.migrations_dir = migrations_dir
        self.migration_table = "schema_migrations"

    async def init_migration_table(self) -> None:
        """
        Создает таблицу для отслеживания миграций.
        """
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.migration_table} (
            id SERIAL PRIMARY KEY,
            version VARCHAR(20) UNIQUE NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        await self.database.execute(query)
        print("Таблица миграций создана")

    async def get_applied_migrations(self) -> list:
        """
        Получает список уже примененных миграций.

        Returns:
            list: Список версий примененных миграций
        """
        query = f"SELECT version FROM {self.migration_table} ORDER BY version"
        rows = await self.database.fetch(query)
        return [row['version'] for row in rows]

    async def mark_migration_as_applied(self, version: str) -> None:
        """
        Помечает миграцию как примененную.

        Args:
            version (str): Версия миграции
        """
        query = f"INSERT INTO {self.migration_table} (version) VALUES ($1)"
        await self.database.execute(query, version)

    async def apply_migration(self, version: str, sql_content: str) -> None:
        """
        Применяет миграцию к базе данных.

        Args:
            version (str): Версия миграции
            sql_content (str): SQL содержимое миграции
        """
        # Выполняем миграцию
        await self.database.execute(sql_content)
        # Помечаем как примененную
        await self.mark_migration_as_applied(version)
        print(f"Миграция {version} успешно применена")

    async def run_migrations(self) -> None:
        """
        Запускает все непримененные миграции.
        """
        # Инициализируем таблицу миграций
        await self.init_migration_table()

        # Получаем список уже примененных миграций
        applied = await self.get_applied_migrations()

        # Получаем список всех файлов миграций
        migration_files = []
        if os.path.exists(self.migrations_dir):
            for filename in sorted(os.listdir(self.migrations_dir)):
                if filename.endswith('.sql'):
                    version = filename.split('_')[0]
                    migration_files.append((version, filename))

        # Применяем непримененные миграции
        for version, filename in migration_files:
            if version not in applied:
                file_path = os.path.join(self.migrations_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    sql_content = f.read()

                print(f"Применяется миграция {version}...")
                await self.apply_migration(version, sql_content)

        print("Все миграции применены")