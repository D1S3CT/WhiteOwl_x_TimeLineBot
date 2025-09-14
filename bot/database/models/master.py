"""
Модель мастера и методы работы с ней.
"""

from datetime import datetime
from bot.database.database import Database


class Master:
    """
    Модель мастера.
    """

    def __init__(self, id: int = None, first_name: str = "", last_name: str = "",
                 phone_number: str = "", specialization: str = "",
                 photo_url: str = None, description: str = "",
                 experience_years: int = 0, created_at: datetime = None,
                 updated_at: datetime = None):
        """
        Инициализирует объект мастера.

        Args:
            id (int, optional): ID мастера
            first_name (str): Имя мастера
            last_name (str): Фамилия мастера
            phone_number (str): Номер телефона
            specialization (str): Специализация
            photo_url (str, optional): URL фотографии
            description (str): Описание мастера
            experience_years (int): Стаж в годах
            created_at (datetime, optional): Дата создания
            updated_at (datetime, optional): Дата обновления
        """
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.specialization = specialization
        self.photo_url = photo_url
        self.description = description
        self.experience_years = experience_years
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    async def create(cls, db: Database, first_name: str, last_name: str,
                     phone_number: str, specialization: str, description: str = "",
                     experience_years: int = 0, photo_url: str = None) -> 'Master':
        """
        Создает нового мастера в базе данных.

        Args:
            db (Database): Объект подключения к базе данных
            first_name (str): Имя мастера
            last_name (str): Фамилия мастера
            phone_number (str): Номер телефона
            specialization (str): Специализация
            description (str): Описание мастера
            experience_years (int): Стаж в годах
            photo_url (str, optional): URL фотографии

        Returns:
            Master: Созданный объект мастера
        """
        query = """
        INSERT INTO masters (first_name, last_name, phone_number, specialization, 
                           photo_url, description, experience_years)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id, created_at, updated_at
        """

        row = await db.fetchrow(query, first_name, last_name, phone_number,
                                specialization, photo_url, description, experience_years)

        master = cls(
            id=row['id'],
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            specialization=specialization,
            photo_url=photo_url,
            description=description,
            experience_years=experience_years,
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )

        return master

    @classmethod
    async def get_by_id(cls, db: Database, master_id: int) -> 'Master':
        """
        Получает мастера по ID.

        Args:
            db (Database): Объект подключения к базе данных
            master_id (int): ID мастера

        Returns:
            Master: Объект мастера или None, если не найден
        """
        query = """
        SELECT id, first_name, last_name, phone_number, specialization, 
               photo_url, description, experience_years, created_at, updated_at
        FROM masters
        WHERE id = $1
        """

        row = await db.fetchrow(query, master_id)
        if not row:
            return None

        return cls(**row)

    @classmethod
    async def get_by_phone(cls, db: Database, phone_number: str) -> 'Master':
        """
        Получает мастера по номеру телефона.

        Args:
            db (Database): Объект подключения к базе данных
            phone_number (str): Номер телефона

        Returns:
            Master: Объект мастера или None, если не найден
        """
        query = """
        SELECT id, first_name, last_name, phone_number, specialization, 
               photo_url, description, experience_years, created_at, updated_at
        FROM masters
        WHERE phone_number = $1
        """

        row = await db.fetchrow(query, phone_number)
        if not row:
            return None

        return cls(**row)

    async def update(self, db: Database) -> None:
        """
        Обновляет информацию о мастере в базе данных.

        Args:
            db (Database): Объект подключения к базе данных
        """
        query = """
        UPDATE masters
        SET first_name = $1, last_name = $2, phone_number = $3, specialization = $4,
            photo_url = $5, description = $6, experience_years = $7, updated_at = NOW()
        WHERE id = $8
        """

        await db.execute(query, self.first_name, self.last_name, self.phone_number,
                         self.specialization, self.photo_url, self.description,
                         self.experience_years, self.id)

    async def delete(self, db: Database) -> None:
        """
        Удаляет мастера из базы данных.

        Args:
            db (Database): Объект подключения к базе данных
        """
        query = "DELETE FROM masters WHERE id = $1"
        await db.execute(query, self.id)