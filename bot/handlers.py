from typing import List, Tuple, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import (
    logger, get_message, is_admin, MAX_MESSAGE_LENGTH, YOUR_CHAT_ID
)
from database import (
    save_user, get_user_language, update_user_language,
    user_has_active_message, set_user_active_message,
    save_message, save_reply, get_unanswered_messages,
    get_user_messages, get_all_users, db_connection
)
from keyboards import (
    get_message_type_keyboard, get_admin_main_keyboard,
    get_unanswered_message_keyboard, get_language_keyboard, add_back_button
)


async def send_message_safe(bot: Any, chat_id: int,
                            text: str, **kwargs) -> None:
    """
    Безопасная отправка сообщения с обработкой ошибок.
    Sending messages safely with error handling.
    """
    try:
        await bot.send_message(chat_id=chat_id, text=text, **kwargs)
    except Exception as e:
        logger.error(f'Failed to send message to {chat_id}: {e}')
        raise


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start.
    /start command handler.
    """
    if not update.message or not update.message.from_user:
        logger.warning('Invalid start command received')
        return

    user = update.effective_user
    save_user(user)
    lang = get_user_language(user.id)

    # Разделение логики для админа и обычных пользователей / Separation of
    # logic for admin and regular users
    if is_admin(update.effective_chat.id):
        await send_message_safe(
            context.bot,
            update.effective_chat.id,
            get_message('start_admin', lang),
            reply_markup=get_admin_main_keyboard(lang)
        )
    else:
        # Проверка наличия неотвеченных сообщений у пользователя / Checking if
        # a user has any unanswered messages
        if user_has_active_message(user.id):
            await send_message_safe(
                context.bot,
                update.effective_chat.id,
                get_message('active_message', lang),
                reply_markup=None
            )
        else:
            await send_message_safe(
                context.bot,
                update.effective_chat.id,
                get_message('start_user', lang, name=user.first_name),
                reply_markup=get_message_type_keyboard(lang)
            )


async def set_language(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды для смены языка.
    Command handler for changing language.
    """
    user = update.effective_user
    lang = get_user_language(user.id)

    if update.message:
        await update.message.delete()

    await send_message_safe(
        context.bot,
        update.effective_chat.id,
        get_message('choose_language', lang),
        reply_markup=get_language_keyboard(lang)
    )


async def language_callback(update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик callback для смены языка.
    Callback handler for changing language.
    """
    query = update.callback_query
    await query.answer()

    # Извлекаем выбранный язык (формат: 'set_lang_ru' -> 'ru') / Extract the
    # selected language (format: 'set_lang_ru' -> 'ru')
    lang = query.data.split('_')[-1]
    user_id = query.from_user.id
    update_user_language(user_id, lang)

    new_lang = get_user_language(user_id)

    try:
        await query.delete_message()

        # Показываем обновленный интерфейс / Showing the updated interface
        if is_admin(user_id):
            # Админский интерфейс / Admin interface
            await send_message_safe(
                context.bot,
                user_id,
                get_message('language_set', new_lang),
                reply_markup=get_admin_main_keyboard(new_lang)
            )
        else:
            # Пользовательский интерфейс / User interface
            await send_message_safe(
                context.bot,
                user_id,
                get_message('language_set', new_lang),
                reply_markup=get_message_type_keyboard(new_lang)
            )
    except Exception as e:
        logger.error(f'Error in language change: {e}')
        await send_message_safe(
            context.bot,
            user_id,
            get_message('language_set', new_lang),
            reply_markup=(
                get_admin_main_keyboard(new_lang) if is_admin(user_id)
                    else get_message_type_keyboard(new_lang)
            )
        )


async def handle_user_message(update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик входящих от пользователей сообщений.
    Handler for incoming messages from users.
    """
    # Фильтрация пустых сообщений и сообщений от админа / Filtering empty
    # messages and messages from the admin
    if not update.message or not update.message.text:
        logger.warning('Empty message received')
        return

    if is_admin(update.effective_chat.id):
        return

    # Получение информации о пользователе / Getting user information
    user = update.effective_user
    user_id = user.id
    lang = get_user_language(user_id)
    user_message = update.message.text.strip()

    # Обработка команды смены языка / Processing the language change command
    if user_message == get_message('change_language', lang):
        await set_language(update, context)
        return

    # Валидация сообщения / Message validation
    if not user_message:
        await send_message_safe(
            context.bot,
            update.effective_chat.id,
            get_message('empty_message', lang)
        )
        return

    if len(user_message) > MAX_MESSAGE_LENGTH:
        await send_message_safe(
            context.bot,
            update.effective_chat.id,
            get_message('message_too_long', lang,
                      max_length=MAX_MESSAGE_LENGTH)
        )
        return

    # Проверка наличия активного сообщения / Checking for an active message
    if user_has_active_message(user_id):
        await send_message_safe(
            context.bot,
            update.effective_chat.id,
            get_message('active_message', lang),
            reply_markup=None
        )
        return

    # Определение выбранного типа сообщения / Defining the selected
    # message type
    message_type_keys = ['suggestion', 'complaint', 'message']
    selected_type = None

    button_texts = {
        type_key: get_message(f'message_types.{type_key}.button', lang) for
            type_key in message_type_keys
    }

    for type_key, button_text in button_texts.items():
        if user_message == button_text:
            selected_type = type_key
            break

    # Если тип сообщения выбран - просим ввести сообщение / If the message
    # type is selected, please enter a message
    if selected_type:
        context.user_data['message_type'] = selected_type
        await send_message_safe(
            context.bot,
            update.effective_chat.id,
            get_message(
                'enter_message',
                lang,
                type=get_message(
                    f'message_types.{selected_type}.display', lang)
            ),
            reply_markup=None
        )
        return

    # Если пользователь не выбрал тип сообщения - просим выбрать / If the user
    # has not selected the message type, please select
    if 'message_type' not in context.user_data:
        await send_message_safe(
            context.bot,
            update.effective_chat.id,
            get_message('choose_type', lang),
            reply_markup=get_message_type_keyboard(lang)
        )

    try:
        message_type = context.user_data['message_type']
        save_message(user_id, message_type, user_message)
        username = f'@{user.username}' if user.username else f'ID: {user.id}'

        # Отправка уведомления админу / Sending notification to admin
        await send_message_safe(
            context.bot,
            YOUR_CHAT_ID,
            get_message(
                'new_message',
                get_user_language(YOUR_CHAT_ID),
                username=username,
                type=get_message(f'message_types.{message_type}.display',
                                 get_user_language(YOUR_CHAT_ID)),
                text=user_message
            ),
            parse_mode=None,
            reply_markup=get_admin_main_keyboard(
                get_user_language(YOUR_CHAT_ID))
        )

        # Подтверждение пользователю об отправке / Confirmation to the user
        # about sending
        await send_message_safe(
            context.bot,
            update.effective_chat.id,
            get_message('message_sent', lang),
            reply_markup=None
        )
    except Exception as e:
        logger.error(f'Error processing message: {e}')
        set_user_active_message(user_id, False)
        await send_message_safe(
            context.bot,
            update.effective_chat.id,
            get_message('error', lang)
        )
    finally:
        # Очистка временных данных / Clearing temporary data
        if 'message_type' in context.user_data:
            del context.user_data['message_type']


async def handle_admin_callback(update: Update,
                              context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Главный обработчик callback-запросов от администратора.
    The main handler of callback requests from the administrator.
    """
    query = update.callback_query
    await query.answer()

    # Проверка прав администратора / Checking administrator rights
    if not is_admin(update.effective_chat.id):
        logger.warning(
            f'Non-admin access attempt from {update.effective_chat.id}')
        return

    lang = get_user_language(query.from_user.id)

    try:
        # Обработчик смены языка / Language change handler
        if query.data == 'change_language':
            await query.edit_message_text(
                get_message('choose_language', lang),
                reply_markup=get_language_keyboard(lang)
            )
            return

        # Просмотр неотвеченных сообщений / View unanswered messages
        if query.data == 'unanswered':
            messages = get_unanswered_messages()
            if not messages:
                await query.edit_message_text(
                    get_message('no_unanswered', lang),
                    reply_markup=get_admin_main_keyboard(lang)
                )
                return

            # Формируем список кнопок с неотвеченными сообщениями / Forming a
            # list of buttons with unanswered messages
            keyboard = []
            no_name_text = get_message('no_name', lang)
            for msg in messages[:10]:
                btn_text = f'{msg[2] or msg[3] or no_name_text} - {msg[4]}'
                keyboard.append([InlineKeyboardButton(
                    btn_text,
                    callback_data=f'view_msg_{msg[0]}_{msg[1]}')
                ])

            await query.edit_message_text(
                get_message('unanswered_messages', lang),
                reply_markup=InlineKeyboardMarkup(
                    add_back_button(keyboard, lang))
            )

        # Просмотр конкретного сообщения / View a specific message
        elif query.data.startswith('view_msg_'):
            parts = query.data.split('_')
            message_id = int(parts[2])
            user_id = int(parts[3])

            with db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT m.message_type, m.message_text, m.created_at,
                       u.username, u.first_name
                FROM messages m
                JOIN users u ON m.user_id = u.user_id
                WHERE m.id = ?
                ''', (message_id,))
                message = cursor.fetchone()

            if message:
                # Форматируем и показываем сообщение / Format and display
                # the message
                no_name_text = get_message('no_name', lang)
                await query.edit_message_text(
                    get_message(
                        'message_from',
                        lang,
                        name=message[4] or message[3] or no_name_text,
                        type=message[0],
                        text=message[1],
                        time=message[2]
                    ),
                    parse_mode='Markdown',
                    reply_markup=get_unanswered_message_keyboard(
                        message_id, lang)
                )

        # Обработчик ответа на сообщение / Message response handler
        elif query.data.startswith('reply_msg_'):
            message_id = int(query.data.split('_')[2])
            context.user_data['reply_to'] = {'message_id': message_id}
            await query.edit_message_text(
                get_message('enter_reply', lang),
                reply_markup=None
            )

        # Обработчик истории сообщений / Message history handler
        elif query.data == 'history':
            users = get_all_users()
            if not users:
                await query.edit_message_text(
                    get_message('no_history', lang),
                    reply_markup=get_admin_main_keyboard(lang)
                )
                return

            context.user_data['history_page'] = 0
            await show_history_page(query, context, users, lang)

        # Навигация по страницам истории / Navigating through history pages
        elif query.data.startswith('history_page_'):
            page = int(query.data.split('_')[2])
            users = get_all_users()
            await show_history_page(query, context, users, lang, page)

        # Просмотр сообщений конкретного пользователя / View messages from a
        # specific user
        elif query.data.startswith('user_'):
            parts = query.data.split('_')
            user_id = int(parts[1])
            page = int(parts[2]) if len(parts) > 2 else 0

            messages = get_user_messages(user_id)
            await show_user_messages_page(query, user_id, messages, lang, page)

        # Обработчик ответа пользователю (из истории сообщений) / User
        # response handler (from message history)
        elif query.data.startswith('reply_'):
            user_id = int(query.data.split('_')[1])
            context.user_data['reply_to'] = {'user_id': user_id}
            await query.edit_message_text(
                get_message('enter_reply', lang),
                reply_markup=None
            )

        # Обработка возврата в главное меню / Processing return to main menu
        elif query.data == 'back_to_main':
            await query.edit_message_text(
                get_message('start_admin', lang),
                reply_markup=get_admin_main_keyboard(lang)
            )

    except Exception as e:
        logger.error(f'Error in admin callback: {e}')
        await query.edit_message_text(
            get_message('error', lang),
            reply_markup=get_admin_main_keyboard(lang)
        )


async def show_history_page(
        query: Any, context: ContextTypes.DEFAULT_TYPE, users: List[Tuple],
        lang: str, page: int = 0) -> None:
    """
    Отображает страницу с историей пользователей с пагинацией.
    Displays a page with user history with pagination.
    """
    # Настройки пагинации / Pagination settings
    ITEMS_PER_PAGE = 5
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    paginated_users = users[start_idx:end_idx]

    # Формирует клавиатуру с пользователями / Generates a keyboard with users
    keyboard = []
    no_name_text = get_message('no_name', lang)
    for user in paginated_users:
        name = user[2] or user[1] or f'{no_name_text} {user[0]}'
        keyboard.append([InlineKeyboardButton(
            name,
            callback_data=f'user_{user[0]}_0'
        )])

    # Добавляет кнопки пагинации / Adds pagination buttons
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton(
            get_message('prev_page', lang),
            callback_data=f'history_page_{page-1}'
        ))
    if end_idx < len(users):
        pagination_buttons.append(InlineKeyboardButton(
            get_message('next_page', lang),
            callback_data=f'history_page_{page+1}'
        ))

    if pagination_buttons:
        keyboard.append(pagination_buttons)

    # Добавляет кнопку возврата в главное меню / Adds a back button to
    # the main menu
    keyboard.append([InlineKeyboardButton(
        get_message('back', lang),
        callback_data='back_to_main'
    )])

    await query.edit_message_text(
        get_message('message_history', lang).split(':')[0] + ':',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    context.user_data['history_page'] = page


async def show_user_messages_page(
        query: Any, user_id: int, messages: List[Tuple],
        lang: str, page: int = 0) -> None:
    """
    Отображает страницу с сообщениями конкретного пользователя с пагинацией.
    Displays a page of messages for a specific user with pagination.
    """
    # Настройки пагинации / Pagination settings
    ITEMS_PER_PAGE = 5
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    paginated_messages = messages[start_idx:end_idx]

    # Формирует текст сообщения с историей переписки / Generates a message
    # text with the correspondence history
    text = get_message('message_history', lang) + '\n\n'
    for msg in paginated_messages:
        message_type = get_message(f'message_types.{msg[0]}.display', lang)
        text += f'📌 {message_type}\n✉️ {msg[1]}\n🕒 {msg[2]}\n'
        if msg[3]:
            text += f'📩 *{get_message("reply", lang)}* {msg[3]}\n🕒 {msg[4]}\n'
        text += '\n'

    keyboard = []

    # Добавляет кнопки пагинации / Adds pagination buttons
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton(
            get_message('prev_page', lang),
            callback_data=f'user_{user_id}_{page-1}'
        ))
    if end_idx < len(messages):
        pagination_buttons.append(InlineKeyboardButton(
            get_message('next_page', lang),
            callback_data=f'user_{user_id}_{page+1}'
        ))

    if pagination_buttons:
        keyboard.append(pagination_buttons)

    # Добавляет кнопку "Ответить" (если у пользователя есть активное
    # сообщение) / Adds a "Reply" button (if the user has an active message)
    if user_has_active_message(user_id):
        keyboard.append([InlineKeyboardButton(
            get_message('enter_reply', lang).split(':')[0],
            callback_data=f'reply_{user_id}'
        )])

    # Добавляет кнопку возврата в главное меню / Adds a back button to the
    # main menu
    keyboard.append([InlineKeyboardButton(
        get_message('back', lang),
        callback_data='back_to_main'
    )])

    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle_admin_reply(update: Update,
                           context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает ответы администратора на сообщения пользователей.
    Processes administrator responses to user messages.
    """
    # Блок проверок безопасности / Security checks
    if not is_admin(update.effective_chat.id):
        logger.warning(
            f'Non-admin reply attempt from {update.effective_chat.id}'
        )
        return

    if 'reply_to' not in context.user_data:
        logger.warning('No reply_to in context')
        return

    if not update.message or not update.message.text:
        logger.warning('Empty admin reply received')
        return

    # Получает данные для ответа / Receives data for response
    reply_data = context.user_data['reply_to']
    reply_text = update.message.text.strip()
    lang = get_user_language(update.effective_user.id)

    # Валидация содержимого ответа / Reply content validation
    if not reply_text:
        await send_message_safe(
            context.bot,
            update.effective_chat.id,
            get_message('empty_message', lang),
            reply_markup=get_admin_main_keyboard(lang)
        )
        return

    if len(reply_text) > MAX_MESSAGE_LENGTH:
        await send_message_safe(
            context.bot,
            update.effective_chat.id,
            get_message('message_too_long', lang,
                        max_length=MAX_MESSAGE_LENGTH),
            reply_markup=get_admin_main_keyboard(lang)
        )
        return

    try:
        with db_connection() as conn:
            cursor = conn.cursor()

            # Сценарий 1: Ответ на конкретное сообщение из истории
            # Scenario 1: Reply to specific message from history
            if 'message_id' in reply_data:
                message_id = reply_data['message_id']
                cursor.execute('''
                SELECT user_id FROM messages WHERE id = ?
                ''', (message_id,))
                result = cursor.fetchone()

                if result:
                    user_id = result[0]
                    user_lang = get_user_language(user_id)
                    save_reply(message_id, reply_text)

                    await send_message_safe(
                        context.bot,
                        user_id,
                        get_message('admin_reply', user_lang, text=reply_text),
                        parse_mode='Markdown'
                    )

                    await send_message_safe(
                        context.bot,
                        update.effective_chat.id,
                        get_message('admin_reply_sent', lang),
                        reply_markup=get_admin_main_keyboard(lang)
                    )

                else:
                    await send_message_safe(
                        context.bot,
                        update.effective_chat.id,
                        get_message('message_not_found', lang),
                        reply_markup=get_admin_main_keyboard(lang)
                    )

            # Сценарий 2: Ответ на последнее неотвеченное сообщение
            # Scenario 2: Reply to latest unanswered message
            elif 'user_id' in reply_data:
                user_id = reply_data['user_id']
                user_lang = get_user_language(user_id)
                cursor.execute('''
                SELECT id FROM messages
                WHERE user_id = ? AND is_answered = FALSE
                ORDER BY created_at DESC LIMIT 1
                ''', (user_id,))
                message = cursor.fetchone()

                if message:
                    save_reply(message[0], reply_text)

                    await send_message_safe(
                        context.bot,
                        user_id,
                        get_message('admin_reply', user_lang, text=reply_text),
                        parse_mode='Markdown'
                    )

                    await send_message_safe(
                        context.bot,
                        update.effective_chat.id,
                        get_message('admin_reply_sent', lang),
                        reply_markup=get_admin_main_keyboard(lang)
                    )

                else:
                    await send_message_safe(
                        context.bot,
                        update.effective_chat.id,
                        get_message('no_unanswered', lang),
                        reply_markup=get_admin_main_keyboard(lang)
                    )

    except Exception as e:
        logger.error(f'Error sending response: {e}')
        await send_message_safe(
            context.bot,
            update.effective_chat.id,
            get_message('error', lang),
            reply_markup=get_admin_main_keyboard(lang)
        )
    finally:
        # Очистка временных данных / Clearing temporary data
        if 'reply_to' in context.user_data:
            del context.user_data['reply_to']
