from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
)
from config import YOUR_CHAT_ID, TELEGRAM_BOT_TOKEN
from handlers import (
    start, set_language, language_callback, handle_admin_callback,
    handle_admin_reply, handle_user_message
)


def main() -> None:
    """
    Основная функция запуска Telegram бота.
    The main function of launching a Telegram bot.
    """
    # Создание приложения бота с указанным токеном / Create a bot application
    # with the specified token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрация обработчиков / Registering handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('language', set_language))
    application.add_handler(CallbackQueryHandler(language_callback,
                                                 pattern='^set_lang_'))
    application.add_handler(CallbackQueryHandler(handle_admin_callback))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Chat(YOUR_CHAT_ID),
        handle_admin_reply))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & ~filters.Chat(YOUR_CHAT_ID),
        handle_user_message))

    # Запуск бота в режиме постоянного опроса серверов Telegram / Launching
    # a bot in continuous polling mode for Telegram servers
    application.run_polling()


if __name__ == '__main__':
    # Вызывает основную функцию main() для запуска бота / Calls the main()
    # function to start the bot.
    main()
