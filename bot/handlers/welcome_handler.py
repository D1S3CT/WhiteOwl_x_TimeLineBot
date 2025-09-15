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

    welcome_text = (
        "🌟 Добро пожаловать в TimeLineBot! 🌟\n\n"
        "Я помогу вам найти лучшего мастера или стать мастером самому!\n\n"
        "Выберите действие ниже 👇"
    )

    if update.message:
        await update.message.reply_text(
            welcome_text,
            reply_markup=keyboard
        )
    elif update.callback_query:
        await update.callback_query.message.edit_text(
            welcome_text,
            reply_markup=keyboard
        )
        await update.callback_query.answer()


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

    welcome_text = (
        "🌟 Добро пожаловать в TimeLineBot! 🌟\n\n"
        "Я помогу вам найти лучшего мастера или стать мастером самому!\n\n"
        "Выберите действие ниже 👇"
    )

    await update.callback_query.message.edit_text(
        welcome_text,
        reply_markup=keyboard
    )
    await update.callback_query.answer()