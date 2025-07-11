import sqlite3
from contextlib import contextmanager
from typing import Iterator, List, Tuple, Any
from config import logger, MAX_MESSAGE_LENGTH


@contextmanager
def db_connection() -> Iterator[sqlite3.Connection]:
    """
    Контекстный менеджер для работы с базой данных.
    Context manager for working with the database.
    """
    conn = None
    try:
        conn = sqlite3.connect('feedback_bot.db')
        yield conn
    except sqlite3.Error as e:
        logger.error(f'Database error: {e}')
        raise
    finally:
        if conn:
            conn.close()


def init_db() -> None:
    """
    Инициализация базы данных.
    Initializing the database.
    """
    with db_connection() as conn:
        cursor = conn.cursor()

        # Таблица "пользователи" / Table "users"
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            language TEXT DEFAULT 'ru',
            has_active_message BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Таблица "сообщения" / Table "messages"
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message_type TEXT,
            message_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_answered BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')

        # Таблица "ответы" / Table "replies"
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER,
            reply_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (message_id) REFERENCES messages (id)
        )
        ''')

        # Индексы для оптимизации / Indexes for optimization
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_users_user_id
                       ON users(user_id)
        ''')
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_messages_user_id
                       ON messages(user_id)
        ''')
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_messages_is_answered
                       ON messages(is_answered)
        ''')
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_messages_created_at
                       ON messages(created_at)
        ''')
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_replies_message_id
                       ON replies(message_id)
        ''')

        conn.commit()


def get_user_language(user_id: int) -> str:
    """
    Получение языка пользователя из базы данных.
    Getting the user's language from the database.
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT language FROM users WHERE user_id = ?',
                      (user_id,))
        result = cursor.fetchone()
        return result[0] if result else 'ru'


def save_user(user: Any) -> None:
    """
    Сохранение информации о пользователе в базу данных.
    Saving user information to the database.
    """
    if not isinstance(user.id, int) or user.id <= 0:
        raise ValueError('Invalid user ID')

    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name, last_name,
                                   language)
        VALUES (?, ?, ?, ?, ?)
        ''', (user.id, user.username, user.first_name, user.last_name, 'ru'))
        conn.commit()


def update_user_language(user_id: int, language: str) -> None:
    """
    Обновление языка пользователя в базе данных.
    Updating user language in the database.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        return

    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE users SET language = ? WHERE user_id = ?
        ''', (language, user_id))
        conn.commit()


def user_has_active_message(user_id: int) -> bool:
    """
    Проверка наличия активного сообщения у пользователя.
    Check if the user has an active message.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        return False

    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT has_active_message FROM users WHERE user_id = ?
        ''', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else False


def set_user_active_message(user_id: int, has_active: bool) -> None:
    """
    Установка флага активного сообщения для пользователя.
    Sets the active message flag for the user.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        return

    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE users SET has_active_message = ? WHERE user_id = ?
        ''', (has_active, user_id))
        conn.commit()


def save_message(user_id: int, message_type: str, message_text: str) -> int:
    """
    Сохранение сообщения от пользователя в базе данных.
    Saving a message from a user to the database.
    """
    if not all([isinstance(user_id, int), isinstance(message_type, str),
               isinstance(message_text, str)]):
        raise ValueError('Invalid input data')

    if len(message_text) > MAX_MESSAGE_LENGTH:
        raise ValueError('Message too long')

    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO messages (user_id, message_type, message_text)
        VALUES (?, ?, ?)
        ''', (user_id, message_type, message_text))
        message_id = cursor.lastrowid

        cursor.execute('''
        UPDATE users SET has_active_message = TRUE WHERE user_id = ?
        ''', (user_id,))
        conn.commit()
        return message_id


def save_reply(message_id: int, reply_text: str) -> None:
    """
    Сохранение в базе данных ответа администратора на сообщение пользователя.
    Saving the administrator's response to the user's message in the database.
    """
    if not isinstance(message_id, int) or message_id <= 0 or not isinstance(
            reply_text, str):
        raise ValueError('Invalid input data')

    if len(reply_text) > MAX_MESSAGE_LENGTH:
        raise ValueError('Reply too long')

    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO replies (message_id, reply_text)
        VALUES (?, ?)
        ''', (message_id, reply_text))

        cursor.execute('''
        UPDATE messages SET is_answered = TRUE WHERE id = ?
        ''', (message_id,))

        cursor.execute('''
        UPDATE users SET has_active_message = FALSE
        WHERE user_id = (SELECT user_id FROM messages WHERE id = ?)
        ''', (message_id,))
        conn.commit()


def get_unanswered_messages() -> List[Tuple[Any, ...]]:
    """
    Получение списка неотвеченных сообщений.
    Getting a list of unanswered messages.
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT m.id, u.user_id, u.username, u.first_name, m.message_type,
               m.message_text, m.created_at
        FROM messages m
        JOIN users u ON m.user_id = u.user_id
        WHERE m.is_answered = FALSE
        ORDER BY m.created_at
        ''')
        return cursor.fetchall()


def get_user_messages(user_id: int) -> List[Tuple[Any, ...]]:
    """
    Получение истории сообщений пользователя.
    Get user's message history.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        return []

    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT m.message_type, m.message_text, m.created_at, r.reply_text,
                r.created_at
        FROM messages m
        LEFT JOIN replies r ON m.id = r.message_id
        WHERE m.user_id = ?
        ORDER BY m.created_at
        ''', (user_id,))
        return cursor.fetchall()


def get_all_users() -> List[Tuple[Any, ...]]:
    """
    Получение списка всех пользователей, отправивших сообщения.
    Get a list of all users who have sent messages.
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT DISTINCT u.user_id, u.username, u.first_name, u.last_name,
               u.language
        FROM users u
        JOIN messages m ON u.user_id = m.user_id
        ORDER BY u.first_name
        ''')
        return cursor.fetchall()


# Инициализация базы данных / Initializing the database
init_db()
