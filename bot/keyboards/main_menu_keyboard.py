"""
Модуль клавиатуры главного меню бота.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Создает и возвращает inline-клавиатуру главного меню.

    Returns:
        InlineKeyboardMarkup: Inline-клавиатура с основными кнопками
    """
    keyboard = [
        [InlineKeyboardButton("Найти мастера", callback_data="find_master")],
        [InlineKeyboardButton("Мои записи", callback_data="my_appointments")],
        [InlineKeyboardButton("Стать мастером", callback_data="become_master")],
        [InlineKeyboardButton("Помощь", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)