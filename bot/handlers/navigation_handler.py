"""
Обработчики навигации между разделами бота.
"""

from telegram import Update
from telegram.ext import ContextTypes


async def handle_find_master(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик нажатия на кнопку "Найти мастера".

    Args:
        update (Update): Объект обновления от Telegram API
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения команды

    Returns:
        None
    """
    await update.callback_query.message.edit_text(
        "Функция поиска мастеров пока в разработке.",
        reply_markup=update.callback_query.message.reply_markup
    )
    await update.callback_query.answer()


async def handle_my_appointments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик нажатия на кнопку "Мои записи".

    Args:
        update (Update): Объект обновления от Telegram API
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения команды

    Returns:
        None
    """
    await update.callback_query.message.edit_text(
        "Функция просмотра записей пока в разработке.",
        reply_markup=update.callback_query.message.reply_markup
    )
    await update.callback_query.answer()