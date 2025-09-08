"""
Обработчики раздела помощи.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.help_keyboard import get_help_keyboard


async def show_help_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отправляет сообщение с информацией о помощи.

    Args:
        update (Update): Объект обновления от Telegram API
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения команды

    Returns:
        None
    """
    keyboard = get_help_keyboard()
    help_text = "Если тебе нужна помощь, хочешь сообщить об ошибке или поделиться обратной связью, мой мастер всегда на связи!"

    await update.callback_query.message.edit_text(
        help_text,
        reply_markup=keyboard
    )
    await update.callback_query.answer()