"""
Обработчики приветственных сообщений для новых пользователей.
"""

from telegram import Update
from telegram.ext import ContextTypes


async def welcome_new_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик для новых пользователей.

    Автоматически отправляет приветственное сообщение при первом взаимодействии.

    Args:
        update (Update): Объект обновления от Telegram API
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения команды

    Returns:
        None
    """
    await update.message.reply_text("Добро пожаловать! Чем могу помочь?")