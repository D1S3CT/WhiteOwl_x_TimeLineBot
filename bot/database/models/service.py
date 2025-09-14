"""
Модель услуги и методы работы с ней.
"""

from datetime import datetime, timedelta
from bot.database.database import Database


class Service:
    """
    Модель услуги мастера.
    """

    def __init__(self, id: int = None, master_id: int = None, name: str = "",
                 description: str = "", price: str = "", duration: timedelta = None,
                 created_at: datetime = None):
        """
        Инициализирует объект услуги.

        Args:
            id (int, optional): ID услуги
            master_id (int): ID мастера
            name (str): Название услуги
            description (str): Описание услуги
            price (str): Цена услуги
            duration (timedelta, optional): Продолжительность услуги
            created_at (datetime, optional): Дата создания
        """
        self.id = id
        self.master_id = master_id
        self.name = name
        self.description = description
        self.price = price
        self.duration = duration
        self.created_at = created_at

    @classmethod
    async def create(cls, db: Database, master_id: int, name: str,
                     price: str, description: str = "", duration: str = None) -> 'Service':
        """
        Создает новую услугу в базе данных.

        Args:
            db (Database): Объект подключения к базе данных
            master_id (int): ID мастера
            name (str): Название услуги
            price (str): Цена услуги
            description (str): Описание услуги
            duration (str, optional): Продолжительность услуги (в формате 'HH:MM:SS')

        Returns:
            Service: Созданный объект услуги
        """
        query = """
        INSERT INTO services (master_id, name, description, price, duration)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, created_at
        """

        duration_interval = None
        if duration:
            duration_interval = duration  # В PostgreSQL INTERVAL формат

        row = await db.fetchrow(query, master_id, name, description, price, duration_interval)

        service = cls(
            id=row['id'],
            master_id=master_id,
            name=name,
            description=description,
            price=price,
            duration=duration_interval,
            created_at=row['created_at']
        )

        return service

    @classmethod
    async def get_by_master_id(cls, db: Database, master_id: int) -> list:
        """
        Получает все услуги мастера.

        Args:
            db (Database): Объект подключения к базе данных
            master_id (int): ID мастера

        Returns:
            list: Список объектов услуг
        """
        query = """
        SELECT id, master_id, name, description, price, duration, created_at
        FROM services
        WHERE master_id = $1
        ORDER BY created_at
        """

        rows = await db.fetch(query, master_id)
        return [cls(**row) for row in rows]

    @classmethod
    async def get_by_id(cls, db: Database, service_id: int) -> 'Service':
        """
        Получает услугу по ID.

        Args:
            db (Database): Объект подключения к базе данных
            service_id (int): ID услуги

        Returns:
            Service: Объект услуги или None, если не найден
        """
        query = """
        SELECT id, master_id, name, description, price, duration, created_at
        FROM services
        WHERE id = $1
        """

        row = await db.fetchrow(query, service_id)
        if not row:
            return None

        return cls(**row)