"""
Обработчики приветственных сообщений и главного меню.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.main_menu_keyboard import get_main_menu_keyboard


async def show_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = get_main_menu_keyboard()

    welcome_text = (
        "Добро пожаловать! Чем могу помочь?"
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
    keyboard = get_main_menu_keyboard()

    welcome_text = (
        "Добро пожаловать! Чем могу помочь?"
    )

    await update.callback_query.message.edit_text(
        welcome_text,
        reply_markup=keyboard
    )
    await update.callback_query.answer()