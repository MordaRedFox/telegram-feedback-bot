import os
import logging
from typing import Union


# Настройки логгирования / Logging settings
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Конфигурация бота / Bot configuration
YOUR_CHAT_ID = '!!!⚠️ your chat id ⚠️!!!'
TELEGRAM_BOT_TOKEN = '!!!⚠️ your bot token ⚠️!!!'
MAX_MESSAGE_LENGTH = 4000

if YOUR_CHAT_ID is None or TELEGRAM_BOT_TOKEN is None:
    raise ValueError('Required environment variables are not set')

# Локализация / Localization
LOCALES = {
    'ru': {
        # Общие сообщения
        'error': '⚠️ Произошла ошибка при обработке вашего сообщения. '
                'Пожалуйста, попробуйте позже.',
        'empty_message': 'Сообщение не может быть пустым',
        'message_too_long': 'Сообщение слишком длинное. '
                'Максимум {max_length} символов.',
        'no_name': 'Без имени',

        # Сообщения пользователя
        'start_user': 'Привет, {name}! Выберите тип сообщения:',
        'active_message': 'У вас уже есть активное сообщение. '
                    'Дождитесь ответа администратора.',
        'choose_type': 'Пожалуйста, сначала выберите тип сообщения:',
        'enter_message': 'Теперь напишите ваше сообщение типа "{type}":',
        'message_sent': '✅ Ваше сообщение отправлено администратору! '
                'Ожидайте ответа.',
        'admin_reply': '📩 *Ответ от администратора:*\n\n{text}',

        # Сообщения администратора
        'start_admin': 'Панель администратора:',
        'admin_reply_sent': '✅ Ответ отправлен пользователю!',
        'message_not_found': '⚠️ Сообщение не найдено',
        'no_unanswered': '⚠️ Нет неотвеченных сообщений',
        'no_messages': 'Нет сообщений от этого пользователя.',
        'no_history': 'Нет истории переписок.',
        'enter_reply': '✉️ Введите ваш ответ:',
        'unanswered_messages': '📨 Неотвеченные сообщения:',
        'message_history': '📂 История переписки:',
        'new_message': '📩 Новое сообщение\n\n👤 Отправитель: '
                '{username}\n📌 Тип: {type}\n✉️ Текст:\n{text}',
        'message_from': '📩 *Сообщение от {name}*\n\n📌 Тип: {type}\n✉️ '
                'Текст:\n{text}\n🕒 {time}\n',

        # Навигация
        'back': '⬅️ Меню',
        'prev_page': '◀ Предыдущая',
        'next_page': 'Следующая ▶',

        # Язык
        'language_set': 'Язык изменён на русский',
        'choose_language': 'Выберите язык:',
        'change_language': '🌐 Сменить язык',
        'languages': {
            'ru': 'Русский',
            'en': 'Английский'
        },

        # Типы сообщений
        'message_types': {
            'suggestion': {
                'button': '💡 Предложение',
                'display': 'Предложение'
            },
            'complaint': {
                'button': '🚫 Жалоба',
                'display': 'Жалоба'
            },
            'message': {
                'button': '💬 Сообщение',
                'display': 'Сообщение'
            }
        },

        # Прочее
        'reply': 'Ответ'
    },
    'en': {
        # Common messages
        'error': '⚠️ An error occurred while processing your message. '
                'Please try again later.',
        'empty_message': 'Message cannot be empty',
        'message_too_long': 'Message is too long. '
                'Maximum {max_length} characters.',
        'no_name': 'No name',

        # User messages
        'start_user': 'Hello, {name}! Choose message type:',
        'active_message': 'You already have an active message. '
                'Wait for the administrator\'s response.',
        'choose_type': 'Please select a message type first:',
        'enter_message': 'Now enter your {type} message:',
        'message_sent': '✅ Your message has been sent to the administrator! '
                'Please wait for a response.',
        'admin_reply': '📩 *Reply from admin:*\n\n{text}',

        # Admin messages
        'start_admin': 'Admin panel:',
        'admin_reply_sent': '✅ Reply sent to user!',
        'message_not_found': '⚠️ Message not found',
        'no_unanswered': '⚠️ No unanswered messages',
        'no_messages': 'No messages from this user.',
        'no_history': 'No message history.',
        'enter_reply': '✉️ Enter your reply:',
        'unanswered_messages': '📨 Unanswered messages:',
        'message_history': '📂 Message history:',
        'new_message': '📩 New message\n\n👤 From: {username}\n📌 '
                'Type: {type}\n✉️ Text:\n{text}',
        'message_from': '📩 *Message from {name}*\n\n📌 Type: {type}\n✉️ '
                'Text:\n{text}\n🕒 {time}\n',

        # Navigation
        'back': '⬅️ Menu',
        'prev_page': '◀ Previous',
        'next_page': 'Next ▶',

        # Language
        'language_set': 'Language has been set to English',
        'choose_language': 'Choose language:',
        'change_language': '🌐 Change language',
        'languages': {
            'ru': 'Russian',
            'en': 'English'
        },

        # Message types
        'message_types': {
            'suggestion': {
                'button': '💡 Suggestion',
                'display': 'Suggestion'
            },
            'complaint': {
                'button': '🚫 Complaint',
                'display': 'Complaint'
            },
            'message': {
                'button': '💬 Message',
                'display': 'Message'
            }
        },

        # Miscellaneous
        'reply': 'Reply'
    }
}


def get_message(key: str, lang: str = 'ru', **kwargs) -> Union[str, dict]:
    """
    Возвращает локализованное сообщение с подстановкой параметров.
    Returns a localized message with parameter substitution.
    """
    locale = LOCALES.get(lang, LOCALES['ru'])
    msg = locale

    try:
        # Обработка вложенных ключей через точку / Processing nested keys
        # through dot
        keys = key.split('.')
        for k in keys:
            msg = msg.get(k, {})

        # Если запрашивается конкретный subkey / If a specific subkey
        # is requested
        if 'subkey' in kwargs:
            subkey = kwargs['subkey']
            return msg.get(subkey, {})

        # Если результат - строка, форматируем её / If the result is a string,
        # format it
        if isinstance(msg, str):
            return msg.format(**kwargs) if kwargs else msg

        return msg
    except Exception as e:
        logger.error(f'Error getting message "{key}": {e}')
        return key


def is_admin(chat_id: Union[int, str]) -> bool:
    """
    Проверяет, является ли пользователь администратором.
    Checks if the user is an administrator.
    """
    return int(chat_id) == YOUR_CHAT_ID
