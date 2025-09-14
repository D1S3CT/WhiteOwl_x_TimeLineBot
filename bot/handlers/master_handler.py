"""
Обработчики функционала "Стать мастером".
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.handlers.registration_handler import show_registration_benefits


async def show_become_master_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Показывает опции для становления мастером.

    Args:
        update (Update): Объект обновления от Telegram API
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения команды

    Returns:
        None
    """
    # Перенаправляем к обработчику регистрации
    await show_registration_benefits(update, context)