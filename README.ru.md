<div align="center">

# Telegram Feedback Bot 🤖

## Change language: [English](README.md)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Telegram Bot](https://img.shields.io/badge/Telegram%20Bot-20.0%2B-blue.svg)](https://python-telegram-bot.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🌟 Особенности

<div align="center">

<table>
    <tr>
        <td valign="top" width="50%">
            <h3 align="center">👤 Для пользователей</h3>
            <p align="center">
                <img src="https://img.shields.io/badge/🌐-Мультиязычность-green"
                    alt="Мультиязычность">
                <img src="https://img.shields.io/badge/📩-Отправка%20сообщений-blue"
                    alt="Отправка сообщений">
                <img src="https://img.shields.io/badge/⏳-Одно%20активное%20сообщение-orange"
                    alt="Одно активное сообщение">
            </p>
            <div style="text-align: left; margin-left: 20px;">
                <ul style="text-align: left; padding-left: 20px;">
                    <li>🌐 Поддержка мультиязычности (русский и английский)</li>
                    <li>📩 Отправка сообщений администратору трёх типов:
                        <ul style="text-align: left; padding-left: 20px;">
                            <li>💡 Предложение</li>
                            <li>🚫 Жалоба</li>
                            <li>💬 Сообщение</li>
                        </ul>
                    </li>
                    <li>⏳ Одно активное сообщение (новое можно отправить только после ответа)</li>
                </ul>
            </div>
        </td>
        <td valign="top" width="50%">
            <h3 align="center">👨‍💻 Для администратора</h3>
            <p align="center">
                <img src="https://img.shields.io/badge/🌐-Мультиязычность-green"
                    alt="Мультиязычность">
                <img src="https://img.shields.io/badge/🔔-Просмотр%20сообщений-blue"
                    alt="Просмотр сообщений">
                <img src="https://img.shields.io/badge/✉️-Ответ%20пользователям-orange"
                    alt="Ответ пользователям">
                <img src="https://img.shields.io/badge/📜-История%20переписки-purple"
                    alt="История переписки">
            </p>
            <div style="text-align: left; margin-left: 20px;">
                <ul style="text-align: left; padding-left: 20px;">
                    <li>🌐 Поддержка мультиязычности (русский и английский)</li>
                    <li>🔔 Просмотр неотвеченных сообщений</li>
                    <li>✉️ Ответ на конкретные сообщения</li>
                    <li>📜 Просмотр полной истории переписки с пагинацией</li>
                </ul>
            </div>
        </td>
    </tr>
</table>

</div>

---

## 🛠 Технологии

<div align="center">

<table>
    <tr>
        <th>Компонент</th>
        <th>Версия</th>
        <th>Описание</th>
        <th>Бейдж</th>
    </tr>
    <tr align="center">
        <td>Python</td>
        <td>3.10+</td>
        <td>Основной язык разработки</td>
        <td><img src="https://img.shields.io/badge/Python-310%2B-3776ABlogo=pythonlogoColor=white" alt="Python"></td>
    </tr>
    <tr align="center">
        <td>python-telegram-bot</td>
        <td>20.0+</td>
        <td>API для работы с Telegram</td>
        <td><img src="https://img.shields.io/badge/Telegram%20Bot-20.0%2B-26A5E4?logo=telegram&logoColor=white" alt="Telegram Bot"></td>
    </tr>
    <tr align="center">
        <td>SQLite3</td>
        <td>-</td>
        <td>Хранение данных</td>
        <td><img src="https://img.shields.io/badge/SQLite3-✓-003B57?logo=sqlite&logoColor=white" alt="SQLite3"></td>
    </tr>
    <tr align="center">
        <td>Logging</td>
        <td>-</td>
        <td>Стандартный модуль логирования</td>
        <td><img src="https://img.shields.io/badge/Logging-✓-000000?logo=logging&logoColor=white" alt="Logging"></td>
    </tr>
    <tr align="center">
        <td>Архитектура</td>
        <td>-</td>
        <td>Полностью асинхронная</td>
        <td><img src="https://img.shields.io/badge/Асинхронная-✓-FF6B6B?logo=asynclogoColor=white" alt="Асинхронная"></td>
    </tr>
</table>

</div>

---

## 🔐 Установка и настройка

### 📋 Требования

<div align="center">

<table>
    <tr align="center">
        <th>Требование</th>
        <th>Описание</th>
        <th>Бейдж</th>
    </tr>
    <tr align="center">
        <td>Python</td>
        <td>Версия 3.10 или новее</td>
        <td><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python"></td>
    </tr>
    <tr align="center">
        <td>Telegram</td>
        <td>Аккаунт Telegram</td>
        <td><img src="https://img.shields.io/badge/Telegram-✓-26A5E4?logo=telegram&logoColor=white" alt="Telegram"></td>
    </tr>
    <tr align="center">
        <td>BotFather</td>
        <td>Созданный бот через @BotFather</td>
        <td><img src="https://img.shields.io/badge/BotFather-✓-26A5E4?logo=telegram&logoColor=white" alt="BotFather"></td>
    </tr>
</table>

</div>

### 🔍 Получение Telegram ID
1. Найдите бота @userinfobot в Telegram
2. Отправьте ему команду `/start`
3. Бот ответит вам сообщением с вашим ID (это число вида `123456789`)

### 🔑 Получение токена бота
1. Откройте @BotFather в Telegram
2. Используйте команду `/newbot` для создания нового бота
3. После создания получите токен (выглядит как `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### ⚙️ Настройка конфигурации
Откройте файл `config.py` и замените следующие значения в начале файла:

```python
# Ваш персональный ID администратора (полученный от @userinfobot)
YOUR_CHAT_ID = '!!!⚠️ your chat id ⚠️!!!'  # Замените на ваш ID

# Токен вашего бота (полученный от @BotFather)
TELEGRAM_BOT_TOKEN = '!!!⚠️ your bot token ⚠️!!!'  # Замените на токен бота
```

### 📦 Установка зависимостей
```
pip install -r requirements.txt
```

### 🚀 Запуск бота
```
python main.py
```

---

## 📋 Структура проекта

```
telegram-feedback-bot/
├── bot/
│   ├── config.py         # Конфигурация и локализация
│   ├── database.py       # Модели и работа с БД
│   ├── handlers.py       # Обработчики сообщений
│   ├── keyboards.py      # Генерация клавиатур
│   └── main.py           # Главный исполняемый файл
├── .gitignore            # Игнорируемые файлы для Git
├── bot.log               # Файл логов (создается автоматически)
├── feedback_bot.db       # База данных (создается автоматически)
├── LICENSE               # Лицензия проекта
├── README.md             # Документация на английском
├── README.ru.md          # Документация на русском
└── requirements.txt      # Зависимости
```

---

## 💡 Советы:
- 📊 Все сообщения сохраняются в БД, даже после перезапуска бота
- 🔍 Для просмотра логов проверьте файл bot.log
- ⚡ Файл БД и логов создаются автоматически при первом запуске

## ⚠️ Важное примечание
Этот проект был разработан начинающим программистом-самоучкой. Код может содержать:
- ❌ Ошибки и баги
- ⚡ Неоптимальные решения
- 🛡️ Недочёты в архитектуре

---

## 📩 Контакты
Я открыт для конструктивной критики и предложений по улучшению кода. Если вы нашли ошибку или знаете, как сделать что-то лучше - пожалуйста, свяжитесь со мной!

[![Telegram](https://img.shields.io/badge/-MordaRedFox-0088cc?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/MordaRedFox)
&nbsp;
[![Email](https://img.shields.io/badge/-mordaredfox@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:mordaredfox@gmail.com)
