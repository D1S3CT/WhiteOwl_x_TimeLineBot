"""
Основной модуль Telegram-бота.

Содержит логику инициализации и запуска бота.
"""

from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config.settings import TELEGRAM_BOT_TOKEN
from bot.handlers.welcome_handler import show_welcome_message, show_main_menu
from bot.handlers.help_handler import show_help_message
from bot.handlers.navigation_handler import (
    handle_find_master,
    handle_my_appointments,
    handle_become_master
)


def setup_handlers(application: Application) -> None:
    """
    Регистрирует все обработчики команд и callback-запросов.

    Args:
        application (Application): Объект приложения бота

    Returns:
        None
    """
    # Обработчики команд
    application.add_handler(CommandHandler("start", show_welcome_message))

    # Обработчики callback-запросов
    application.add_handler(CallbackQueryHandler(show_help_message, pattern="^help$"))
    application.add_handler(CallbackQueryHandler(show_main_menu, pattern="^back_to_main$"))
    application.add_handler(CallbackQueryHandler(handle_find_master, pattern="^find_master$"))
    application.add_handler(CallbackQueryHandler(handle_my_appointments, pattern="^my_appointments$"))
    application.add_handler(CallbackQueryHandler(handle_become_master, pattern="^become_master$"))


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