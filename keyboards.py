from typing import List, Union
from telegram import (
    KeyboardButton, ReplyKeyboardMarkup,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from config import get_message, LOCALES


def add_back_button(keyboard: List[List[InlineKeyboardButton]],
                    lang: str = 'ru') -> List[List[InlineKeyboardButton]]:
    """
    Добавляет кнопку 'Назад' в инлайн-клавиатуру, если её ещё нет.
    Adds a 'Back' button to the inline keyboard if not already present.
    """
    # Проверяем, есть ли уже кнопка "Назад" / Check if there is already a
    # "Back" button
    has_back_button = any(
        btn.callback_data == 'back_to_main' for row in keyboard for btn in row
    )

    if not has_back_button:
        keyboard.append([InlineKeyboardButton(
            get_message('back', lang),
            callback_data='back_to_main'
        )])
    return keyboard


def get_message_type_keyboard(lang: str = 'ru') -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру с типами сообщений для обычных пользователей.
    Creates a keyboard with message types for regular users.
    """
    buttons = [
        [KeyboardButton(get_message('message_types', lang,
                                    subkey='suggestion')['button'])],
        [KeyboardButton(get_message('message_types', lang,
                                    subkey='complaint')['button'])],
        [KeyboardButton(get_message('message_types', lang,
                                    subkey='message')['button'])],
        [KeyboardButton(get_message('change_language', lang))]
    ]
    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_admin_main_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """
    Создает главную инлайн-клавиатуру для администратора.
    Creates a main inline keyboard for the administrator.
    """
    keyboard = [
        [InlineKeyboardButton(
            get_message('unanswered_messages', lang).split(':')[0],
            callback_data='unanswered'
        )],
        [InlineKeyboardButton(
            get_message('message_history', lang).split(':')[0],
            callback_data='history'
        )],
        [InlineKeyboardButton(
            get_message('change_language', lang),
            callback_data='change_language'
        )]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_unanswered_message_keyboard(message_id: Union[int, str],
                                    lang: str = 'ru') -> InlineKeyboardMarkup:
    """
    Создает клавиатуру админа для ответа на неотвеченное сообщение.
    Creates an admin keyboard for replying to an unanswered message.
    """
    keyboard = [
        [InlineKeyboardButton(
            get_message('enter_reply', lang).split(':')[0],
            callback_data=f'reply_msg_{message_id}'
        )],
    ]
    return InlineKeyboardMarkup(add_back_button(keyboard, lang))


def get_language_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для выбора языка.
    Creates a keyboard for selecting a language.
    """
    keyboard = []

    for code, name in LOCALES[lang]['languages'].items():
        keyboard.append([InlineKeyboardButton(
            name,
            callback_data=f'set_lang_{code}'
        )])
    return InlineKeyboardMarkup(keyboard)
