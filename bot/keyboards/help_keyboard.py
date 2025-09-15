"""
Модуль клавиатуры раздела помощи.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_help_keyboard() -> InlineKeyboardMarkup:
    """
    Создает и возвращает inline-клавиатуру раздела помощи.

    Returns:
        InlineKeyboardMarkup: Inline-клавиатура с кнопкой помощи
    """
    keyboard = [
        [InlineKeyboardButton("💬 Связаться с создателем", url="https://t.me/D1S3CT")],
        [InlineKeyboardButton("↩️ Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)