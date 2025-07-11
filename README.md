# Feedback Bot 🤖

**Choose language:**
[English](README.md) | [Русский](README.ru.md)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Telegram Bot](https://img.shields.io/badge/Telegram%20Bot-20.0%2B-blue.svg)](https://python-telegram-bot.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Telegram bot for feedback between users and the administrator with multilingual support and a flexible localization system.

## 🌟 Key Features

### 👤 For Users
- 📩 Send three types of messages to admin:
  - 💡 Suggestion
  - 🚫 Complaint
  - 💬 Message
- 🌐 Multilingual support (Russian/English)
- ⏳ Single active message system (must wait for reply before sending new messages)

### 👨‍💻 For Admin
- 🔔 View pending/unanswered messages
- ✉️ Direct replies to specific messages
- 📜 Full message history with pagination
- 🌐 Multilingual interface (Russian/English)

## How the Bot Works

### 🔹 For Users:
- User sends a message through the bot  
- They get an **active message** (awaiting response)  
- While the active message is pending, the user **cannot** send new messages  

### 🔹 For Admin:
- Can **reply** to users' unanswered messages  
- Has access to **message history** with each user  
- Can respond to pending messages **via conversation history**

## 🛠 Technologies

| Component            | Version      | Description                          |
|----------------------|--------------|--------------------------------------|
| Python               | 3.10+        | Core development language            |
| python-telegram-bot  | 20.0+        | Telegram API framework               |
| SQLite3              | -            | Data storage                         |
| Logging              | -            | Standard logging module              |
| Architecture         | -            | Fully asynchronous                   |

## ⚙️ Installation & Setup

### Requirements
1. Python 3.10 or newer
2. Telegram account
3. Bot created via @BotFather

### Getting Your Telegram ID
1. Locate the @userinfobot in Telegram
2. Send it the `/start` command
3. The bot will reply with your Telegram ID (a numeric value like `123456789`)

### Obtaining Bot Token
1. Open @BotFather in Telegram
2. Use the `/newbot` command to create a new bot
3. Upon creation, you'll receive an access token (format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### Configuration Setup
Open the `config.py` file and modify these values at the top of the file:

```python
# Your admin user ID (obtained from @userinfobot)
YOUR_CHAT_ID = '!!!⚠️ your chat id ⚠️!!!'  # Replace with your ID

# Your bot token (obtained from @BotFather)
TELEGRAM_BOT_TOKEN = '!!!⚠️ your bot token ⚠️!!!'  # Replace with your bot token
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### 🚀 Launch the bot
```bash
python main.py
```

## 📋 Project structure
```
feedback-bot/
├── config.py         # Configuration and localization
├── database.py       # Models and database operations
├── handlers.py       # Message handlers
├── keyboards.py      # Keyboard generation
├── main.py           # Entry point
├── requirements.txt  # Dependencies
├── feedback_bot.db   # Database (auto-created)
└── bot.log           # Log file (auto-created)
```

## 💡 Tips:
- All messages are saved to the database, even after bot restart
- Check the bot.log file to view logs
- The database and log files are created automatically on first launch

## ⚠️ Important Note
This project was developed by a self-taught beginner programmer. The code may contain:
- Errors and bugs
- Suboptimal solutions
- Architectural imperfections

I'm open to constructive criticism and code improvement suggestions. If you find an error or know how to improve something - please create an issue or pull request!
