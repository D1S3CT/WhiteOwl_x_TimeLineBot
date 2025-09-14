"""
Обработчики процесса регистрации мастера.
"""

import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.keyboards.registration_keyboard import (
    get_registration_start_keyboard,
    get_registration_benefits_text,
    get_terms_agreement_keyboard,
    get_terms_text,
    get_back_to_terms_keyboard,
    get_full_name_input_text
)
from bot.keyboards.main_menu_keyboard import get_main_menu_keyboard


async def show_registration_benefits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Показывает сообщение с преимуществами регистрации мастера.

    Args:
        update (Update): Объект обновления от Telegram API
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения команды

    Returns:
        None
    """
    keyboard = get_registration_start_keyboard()
    text = get_registration_benefits_text()

    # Если это callback query, обновляем сообщение
    if update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=keyboard)
        await update.callback_query.answer()
    else:
        # Если это обычное сообщение, отправляем новое
        await update.message.reply_text(text, reply_markup=keyboard)


async def start_master_registration_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Начинает процесс регистрации мастера - показывает условия использования.

    Args:
        update (Update): Объект обновления от Telegram API
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения команды

    Returns:
        None
    """
    keyboard = get_terms_agreement_keyboard()
    text = get_terms_text()

    await update.callback_query.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await update.callback_query.answer()


async def handle_terms_acceptance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает согласие пользователя с условиями.

    Args:
        update (Update): Объект обновления от Telegram API
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения команды

    Returns:
        None
    """
    # Пользователь согласился с условиями
    # Переходим к вводу ФИО
    keyboard = get_back_to_terms_keyboard()
    text = get_full_name_input_text()

    # Устанавливаем флаг, что пользователь находится на этапе ввода ФИО
    context.user_data['registration_step'] = 'full_name_input'

    await update.callback_query.message.edit_text(
        text,
        reply_markup=keyboard
    )
    await update.callback_query.answer()


async def handle_full_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает ввод ФИО пользователя.

    Args:
        update (Update): Объект обновления от Telegram API
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения команды

    Returns:
        None
    """
    # Проверяем, что пользователь действительно на этапе ввода ФИО
    if context.user_data.get('registration_step') != 'full_name_input':
        return

    full_name = update.message.text.strip()

    # Валидация ФИО
    if not validate_full_name(full_name):
        await update.message.reply_text(
            "❌ Пожалуйста, введите корректные Фамилию и Имя (только буквы, пробелы и дефисы, минимум 2 слова):"
        )
        return

    # Сохраняем ФИО в контексте пользователя
    context.user_data['temp_master_data'] = {
        'full_name': full_name
    }

    # Переходим к следующему шагу (пока показываем заглушку)
    keyboard = [[InlineKeyboardButton("« Назад", callback_data="back_to_full_name_input")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"✅ Отлично, {full_name}!\n\n"
        "Следующий шаг регистрации в разработке.\n"
        "Скоро здесь появится возможность продолжить регистрацию!",
        reply_markup=reply_markup
    )

    # Сбрасываем флаг этапа
    context.user_data['registration_step'] = None


def validate_full_name(full_name: str) -> bool:
    """
    Валидирует введенное ФИО.

    Args:
        full_name (str): Введенное ФИО

    Returns:
        bool: True если ФИО корректно, False если нет
    """
    if not full_name or len(full_name.strip()) < 3:
        return False

    # Проверяем, что есть хотя бы два слова
    words = full_name.split()
    if len(words) < 2:
        return False

    # Проверяем, что содержит только буквы, пробелы и дефисы
    pattern = r'^[а-яА-ЯёЁa-zA-Z\s\-]+$'
    if not re.match(pattern, full_name):
        return False

    # Проверяем длину каждого слова
    for word in words:
        if len(word.strip()) < 2:
            return False

    return True


async def handle_terms_decline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает отказ пользователя от условий.

    Args:
        update (Update): Объект обновления от Telegram API
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения команды

    Returns:
        None
    """
    # Пользователь отказался от условий - возвращаем в главное меню
    keyboard = get_main_menu_keyboard()

    await update.callback_query.message.edit_text(
        "Добро пожаловать! Чем могу помочь?",
        reply_markup=keyboard
    )
    await update.callback_query.answer()


async def return_to_main_menu_from_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Возвращает пользователя в главное меню из процесса регистрации.

    Args:
        update (Update): Объект обновления от Telegram API
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения команды

    Returns:
        None
    """
    # Очищаем данные регистрации
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
    """
    Возвращает пользователя к условиям из процесса регистрации.

    Args:
        update (Update): Объект обновления от Telegram API
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения команды

    Returns:
        None
    """
    # Очищаем данные текущего шага
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