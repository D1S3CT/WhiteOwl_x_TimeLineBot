"""
Обработчики процесса регистрации мастера.
"""

import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.keyboards.registration_keyboard import (
    get_registration_start_keyboard,
    get_terms_agreement_keyboard,
    get_back_to_terms_keyboard
)
from bot.keyboards.main_menu_keyboard import get_main_menu_keyboard
from bot.texts.registrations_texts import (
    get_registration_benefits_text,
    get_terms_text,
    get_full_name_input_text
)


async def show_registration_benefits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает сообщение с преимуществами регистрации мастера."""
    keyboard = get_registration_start_keyboard()
    text = get_registration_benefits_text()

    if update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=keyboard)
        await update.callback_query.answer()
    else:
        await update.message.reply_text(text, reply_markup=keyboard)


async def start_master_registration_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Начинает процесс регистрации мастера - показывает условия использования."""
    keyboard = get_terms_agreement_keyboard()
    text = get_terms_text()

    await update.callback_query.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await update.callback_query.answer()


async def handle_terms_acceptance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает согласие пользователя с условиями."""
    keyboard = get_back_to_terms_keyboard()
    text = get_full_name_input_text()

    context.user_data['registration_step'] = 'full_name_input'

    await update.callback_query.message.edit_text(
        text,
        reply_markup=keyboard
    )
    await update.callback_query.answer()


async def handle_full_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает ввод ФИО пользователя."""
    if context.user_data.get('registration_step') != 'full_name_input':
        return

    full_name = update.message.text.strip()

    if not validate_full_name(full_name):
        await update.message.reply_text(
            "❌ Пожалуйста, введите корректные Фамилию и Имя (только буквы, пробелы и дефисы, минимум 2 слова):"
        )
        return

    context.user_data['temp_master_data'] = {
        'full_name': full_name
    }

    keyboard = [[InlineKeyboardButton("« Назад", callback_data="back_to_full_name_input")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"✅ Отлично, {full_name}!\n\n"
        "Следующий шаг регистрации в разработке.\n"
        "Скоро здесь появится возможность продолжить регистрацию!",
        reply_markup=reply_markup
    )

    context.user_data['registration_step'] = None


def validate_full_name(full_name: str) -> bool:
    """Валидирует введенное ФИО."""
    if not full_name or len(full_name.strip()) < 3:
        return False

    words = full_name.split()
    if len(words) < 2:
        return False

    pattern = r'^[а-яА-ЯёЁa-zA-Z\s\-]+$'
    if not re.match(pattern, full_name):
        return False

    for word in words:
        if len(word.strip()) < 2:
            return False

    return True


async def handle_terms_decline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает отказ пользователя от условий."""
    keyboard = get_main_menu_keyboard()

    await update.callback_query.message.edit_text(
        "🌟 Добро пожаловать в TimeLineBot! 🌟\n\n"
        "Я помогу вам найти лучшего мастера или стать мастером самому!\n\n"
        "Выберите действие ниже 👇",
        reply_markup=keyboard
    )
    await update.callback_query.answer()


async def return_to_main_menu_from_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Возвращает пользователя в главное меню из процесса регистрации."""
    if 'registration_step' in context.user_data:
        del context.user_data['registration_step']
    if 'temp_master_data' in context.user_data:
        del context.user_data['temp_master_data']

    keyboard = get_main_menu_keyboard()

    await update.callback_query.message.edit_text(
        "Добро пожаловать! Чем могу помочь?",
        reply_markup=keyboard
    )
    await update.callback_query.answer()


async def return_to_terms_from_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Возвращает пользователя к условиям из процесса регистрации."""
    if 'registration_step' in context.user_data:
        del context.user_data['registration_step']

    keyboard = get_terms_agreement_keyboard()
    text = get_terms_text()

    await update.callback_query.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await update.callback_query.answer()