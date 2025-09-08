"""
Модуль конфигурации приложения.

Загружает и проверяет конфигурационные параметры из переменных окружения.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Получаем токен из переменной окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в .env файле")