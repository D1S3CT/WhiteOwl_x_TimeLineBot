"""
Модуль клавиатуры регистрации мастера.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_registration_start_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для начала регистрации."""
    keyboard = [
        [InlineKeyboardButton("🚀 Начать регистрацию", callback_data="start_master_registration")],
        [InlineKeyboardButton("🏠 Вернуться в меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_terms_agreement_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для согласия с условиями."""
    keyboard = [
        [InlineKeyboardButton("✅ Согласен", callback_data="accept_terms")],
        [InlineKeyboardButton("❌ Отказаться", callback_data="decline_terms")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_to_terms_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для возврата к условиям."""
    keyboard = [
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_terms")]
    ]
    return InlineKeyboardMarkup(keyboard)