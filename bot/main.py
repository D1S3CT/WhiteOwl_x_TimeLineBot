"""
Основной модуль Telegram-бота.

Содержит логику инициализации и запуска бота.
"""

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config.settings import TELEGRAM_BOT_TOKEN
from bot.handlers.welcome_handler import show_welcome_message, show_main_menu
from bot.handlers.help_handler import show_help_message
from bot.handlers.registration_handler import (
    show_registration_benefits,
    start_master_registration_process,
    handle_terms_acceptance,
    handle_terms_decline,
    return_to_main_menu_from_registration,
    return_to_terms_from_registration,
    handle_full_name_input
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

    # Обработчики callback-запросов главного меню
    application.add_handler(CallbackQueryHandler(show_help_message, pattern="^help$"))
    application.add_handler(CallbackQueryHandler(show_main_menu, pattern="^back_to_main$"))
    application.add_handler(CallbackQueryHandler(show_registration_benefits, pattern="^become_master$"))

    # Обработчики регистрации мастера
    application.add_handler(CallbackQueryHandler(start_master_registration_process, pattern="^start_master_registration$"))
    application.add_handler(CallbackQueryHandler(handle_terms_acceptance, pattern="^accept_terms$"))
    application.add_handler(CallbackQueryHandler(handle_terms_decline, pattern="^decline_terms$"))
    application.add_handler(CallbackQueryHandler(return_to_main_menu_from_registration, pattern="^back_to_main_from_registration$"))
    application.add_handler(CallbackQueryHandler(return_to_terms_from_registration, pattern="^back_to_terms$"))

    # Обработчик текстовых сообщений для ввода ФИО
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_full_name_input))


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