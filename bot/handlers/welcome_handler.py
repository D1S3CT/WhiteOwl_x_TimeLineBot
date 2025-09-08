"""
Обработчики приветственных сообщений и главного меню.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.main_menu_keyboard import get_main_menu_keyboard


async def show_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отправляет приветственное сообщение с главным меню.

    Args:
        update (Update): Объект обновления от Telegram API
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения команды

    Returns:
        None
    """
    keyboard = get_main_menu_keyboard()

    await update.message.reply_text(
        "Добро пожаловать! Чем могу помочь?",
        reply_markup=keyboard
    )


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Показывает главное меню (используется для возврата из других разделов).

    Args:
        update (Update): Объект обновления от Telegram API
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения команды

    Returns:
        None
    """
    keyboard = get_main_menu_keyboard()

    await update.callback_query.message.edit_text(
        "Добро пожаловать! Чем могу помочь?",
        reply_markup=keyboard
    )
    await update.callback_query.answer()