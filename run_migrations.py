"""
Скрипт для запуска миграций базы данных.
"""

import asyncio
import sys
import os

# Добавляем текущую директорию в путь поиска модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.database.database import Database
from bot.database.migrations import MigrationManager


async def run_migrations():
    """Запускает миграции базы данных."""
    # Создаем подключение к базе данных
    db = Database()

    try:
        # Подключаемся к базе данных
        await db.connect()
        print("Подключение к базе данных установлено")

        # Создаем менеджер миграций
        migration_manager = MigrationManager(db)

        # Запускаем миграции
        await migration_manager.run_migrations()

        print("Миграции успешно применены!")

    except Exception as e:
        print(f"Ошибка при применении миграций: {e}")
        raise
    finally:
        # Закрываем подключение
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(run_migrations())