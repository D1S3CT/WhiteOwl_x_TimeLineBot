"""
Модель графика работы и методы работы с ней.
"""

from datetime import datetime, time
from bot.database.database import Database


class WorkingSchedule:
    """
    Модель графика работы мастера.
    """

    def __init__(self, id: int = None, master_id: int = None, day_of_week: int = None,
                 is_working: bool = True, start_time: time = None, end_time: time = None,
                 break_start_time: time = None, break_end_time: time = None,
                 created_at: datetime = None):
        """
        Инициализирует объект графика работы.

        Args:
            id (int, optional): ID записи графика
            master_id (int): ID мастера
            day_of_week (int): День недели (1=Пн, 7=Вс)
            is_working (bool): Рабочий день или выходной
            start_time (time, optional): Время начала работы
            end_time (time, optional): Время окончания работы
            break_start_time (time, optional): Начало перерыва
            break_end_time (time, optional): Конец перерыва
            created_at (datetime, optional): Дата создания
        """
        self.id = id
        self.master_id = master_id
        self.day_of_week = day_of_week
        self.is_working = is_working
        self.start_time = start_time
        self.end_time = end_time
        self.break_start_time = break_start_time
        self.break_end_time = break_end_time
        self.created_at = created_at

    @classmethod
    async def create(cls, db: Database, master_id: int, day_of_week: int,
                     is_working: bool = True, start_time: str = None,
                     end_time: str = None, break_start_time: str = None,
                     break_end_time: str = None) -> 'WorkingSchedule':
        """
        Создает запись графика работы в базе данных.

        Args:
            db (Database): Объект подключения к базе данных
            master_id (int): ID мастера
            day_of_week (int): День недели (1=Пн, 7=Вс)
            is_working (bool): Рабочий день или выходной
            start_time (str, optional): Время начала работы (формат 'HH:MM')
            end_time (str, optional): Время окончания работы (формат 'HH:MM')
            break_start_time (str, optional): Начало перерыва (формат 'HH:MM')
            break_end_time (str, optional): Конец перерыва (формат 'HH:MM')

        Returns:
            WorkingSchedule: Созданный объект графика работы
        """
        query = """
        INSERT INTO working_schedules (master_id, day_of_week, is_working, 
                                     start_time, end_time, break_start_time, break_end_time)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id, created_at
        """

        row = await db.fetchrow(query, master_id, day_of_week, is_working,
                                start_time, end_time, break_start_time, break_end_time)

        schedule = cls(
            id=row['id'],
            master_id=master_id,
            day_of_week=day_of_week,
            is_working=is_working,
            start_time=start_time,
            end_time=end_time,
            break_start_time=break_start_time,
            break_end_time=break_end_time,
            created_at=row['created_at']
        )

        return schedule

    @classmethod
    async def get_by_master_id(cls, db: Database, master_id: int) -> list:
        """
        Получает график работы мастера.

        Args:
            db (Database): Объект подключения к базе данных
            master_id (int): ID мастера

        Returns:
            list: Список объектов графика работы
        """
        query = """
        SELECT id, master_id, day_of_week, is_working, start_time, end_time,
               break_start_time, break_end_time, created_at
        FROM working_schedules
        WHERE master_id = $1
        ORDER BY day_of_week
        """

        rows = await db.fetch(query, master_id)
        return [cls(**row) for row in rows]

    @classmethod
    async def get_by_master_and_day(cls, db: Database, master_id: int, day_of_week: int) -> 'WorkingSchedule':
        """
        Получает график работы мастера на конкретный день.

        Args:
            db (Database): Объект подключения к базе данных
            master_id (int): ID мастера
            day_of_week (int): День недели (1=Пн, 7=Вс)

        Returns:
            WorkingSchedule: Объект графика работы или None, если не найден
        """
        query = """
        SELECT id, master_id, day_of_week, is_working, start_time, end_time,
               break_start_time, break_end_time, created_at
        FROM working_schedules
        WHERE master_id = $1 AND day_of_week = $2
        """

        row = await db.fetchrow(query, master_id, day_of_week)
        if not row:
            return None

        return cls(**row)