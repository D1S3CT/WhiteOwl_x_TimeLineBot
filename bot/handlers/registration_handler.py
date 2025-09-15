"""
Обработчики процесса регистрации мастера.
"""

import re
from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.registration_keyboard import (
    get_registration_start_keyboard,
    get_terms_agreement_keyboard,
    get_back_to_terms_keyboard,
    get_contact_and_back_keyboard,
    get_remove_keyboard
)
from bot.keyboards.main_menu_keyboard import get_main_menu_keyboard
from bot.texts.registrations_texts import (
    get_registration_benefits_text,
    get_terms_text,
    get_full_name_input_text,
    get_contact_request_text
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
    # Проверяем, что мы на правильном шаге
    if context.user_data.get('registration_step') != 'full_name_input':
        return

    full_name = update.message.text.strip()

    if not validate_full_name(full_name):
        await update.message.reply_text(
            "Пожалуйста, введите корректные Фамилию и Имя (только буквы, пробелы и дефисы, минимум 2 слова):"
        )
        return

    # Инициализируем temp_master_data если его нет
    if 'temp_master_data' not in context.user_data:
        context.user_data['temp_master_data'] = {}

    context.user_data['temp_master_data']['full_name'] = full_name

    # Переходим к следующему шагу - сбор контакта
    text = get_contact_request_text(full_name)
    keyboard = get_contact_and_back_keyboard()

    context.user_data['registration_step'] = 'contact_input'

    await update.message.reply_text(
        text,
        reply_markup=keyboard
    )


async def handle_contact_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает ввод контакта или номера телефона."""
    if context.user_data.get('registration_step') != 'contact_input':
        return

    # Проверяем, была ли нажата кнопка назад
    if update.message.text == "Назад":
        # Возвращаемся к вводу имени
        context.user_data['registration_step'] = 'full_name_input'

        # Очищаем телефон из временных данных если он был
        if 'temp_master_data' in context.user_data and 'phone' in context.user_data['temp_master_data']:
            del context.user_data['temp_master_data']['phone']

        text = get_full_name_input_text()
        keyboard = get_back_to_terms_keyboard()

        await update.message.reply_text(
            text,
            reply_markup=get_remove_keyboard()
        )
        await update.message.reply_text(
            text,
            reply_markup=keyboard
        )
        return

    # Обрабатываем контакт
    if update.message.contact:
        phone = update.message.contact.phone_number
    else:
        phone = update.message.text.strip()
        # Улучшенная валидация номера телефона
        clean_phone = phone.replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if not clean_phone.isdigit() or len(clean_phone) < 10:
            await update.message.reply_text(
                "Пожалуйста, введи корректный номер телефона (например, +79991234567) или нажми кнопку 'Поделиться контактом'.",
                reply_markup=get_contact_and_back_keyboard()
            )
            return

    # Сохраняем контакт во временные данные
    if 'temp_master_data' not in context.user_data:
        context.user_data['temp_master_data'] = {}
    context.user_data['temp_master_data']['phone'] = phone

    # Переход к следующему шагу (пока заглушка)
    await update.message.reply_text(
        f"Спасибо! Мы сохранили твой номер: {phone}",
        reply_markup=get_remove_keyboard()
    )


def validate_full_name(full_name: str) -> bool:
    """Валидирует введенное ФИО."""
    if not full_name or len(full_name.strip()) < 3:
        return False

    words = full_name.split()
    if len(words) < 2:
        return False

    # Проверяем, что каждое слово начинается с буквы
    for word in words:
        if len(word.strip()) < 2 or not word[0].isalpha():
            return False

    pattern = r'^[а-яА-ЯёЁa-zA-Z\s\-]+$'
    return bool(re.match(pattern, full_name))


async def handle_terms_decline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает отказ пользователя от условий."""
    keyboard = get_main_menu_keyboard()

    await update.callback_query.message.edit_text(
        "Добро пожаловать! Чем могу помочь?",
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
    if 'temp_master_data' in context.user_data:
        del context.user_data['temp_master_data']

    keyboard = get_terms_agreement_keyboard()
    text = get_terms_text()

    await update.callback_query.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await update.callback_query.answer()


async def return_to_full_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Возвращает пользователя к вводу ФИО."""
    context.user_data['registration_step'] = 'full_name_input'

    # Очищаем телефон из временных данных если он был
    if 'temp_master_data' in context.user_data and 'phone' in context.user_data['temp_master_data']:
        del context.user_data['temp_master_data']['phone']

    text = get_full_name_input_text()
    keyboard = get_back_to_terms_keyboard()

    await update.callback_query.message.edit_text(
        text,
        reply_markup=keyboard
    )
    await update.callback_query.answer()