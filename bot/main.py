"""
Основной модуль Telegram-бота.

Содержит логику инициализации и запуска бота.
"""

from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config.settings import TELEGRAM_BOT_TOKEN
from bot.handlers.welcome_handler import welcome_new_user


def setup_handlers(application: Application) -> None:
    """
    Регистрирует все обработчики команд и сообщений.

    Args:
        application (Application): Объект приложения бота

    Returns:
        None
    """
    # Обработчик команды /start
    application.add_handler(CommandHandler("start", welcome_new_user))

    # Обработчик первого сообщения от нового пользователя
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, welcome_new_user))


def create_bot_application() -> Application:
    """
    Создает и настраивает приложение бота.

    Returns:
        Application: Настроенное приложение бота

    Raises:
        ValueError: Если TELEGRAM_BOT_TOKEN не установлен
    """
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не установлен в конфигурации")

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    setup_handlers(application)

    return application


def run_bot() -> None:
    """
    Запускает бота в режиме polling.

    Returns:
        None
    """
    application = create_bot_application()
    application.run_polling()


def main() -> None:
    """
    Точка входа в приложение.

    Returns:
        None
    """
    run_bot()