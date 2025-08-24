<div align="center">

# Telegram Feedback Bot 🤖

## Сменить язык: [Русский](README.ru.md)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Telegram Bot](https://img.shields.io/badge/Telegram%20Bot-20.0%2B-blue.svg)](https://python-telegram-bot.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🌟 Features

<div align="center">

<table>
    <tr>
        <td valign="top" width="50%">
            <h3 align="center">👤 For Users</h3>
            <p align="center">
                <img src="https://img.shields.io/badge/🌐-Multilingual-green"
                    alt="Multilingual">
                <img src="https://img.shields.io/badge/📩-Send%20Messages-blue"
                    alt="Send Messages">
                <img src="https://img.shields.io/badge/⏳-One%20Active%20Message-orange"
                    alt="One Active Message">
            </p>
            <div style="text-align: left; margin-left: 20px;">
                <ul style="text-align: left; padding-left: 20px;">
                    <li>🌐 Multilingual support (Russian and English)</li>
                    <li>📩 Send three types of messages to admin:
                        <ul style="text-align: left; padding-left: 20px;">
                            <li>💡 Suggestion</li>
                            <li>🚫 Complaint</li>
                            <li>💬 Message</li>
                        </ul>
                    </li>
                    <li>⏳ One active message (new can be sent only after response)</li>
                </ul>
            </div>
        </td>
        <td valign="top" width="50%">
            <h3 align="center">👨‍💻 For Administrator</h3>
            <p align="center">
                <img src="https://img.shields.io/badge/🌐-Multilingual-green"
                    alt="Multilingual">
                <img src="https://img.shields.io/badge/🔔-View%20Messages-blue"
                    alt="View Messages">
                <img src="https://img.shields.io/badge/✉️-Reply%20to%20Users-orange"
                    alt="Reply to Users">
                <img src="https://img.shields.io/badge/📜-Message%20History-purple"
                    alt="Message History">
            </p>
            <div style="text-align: left; margin-left: 20px;">
                <ul style="text-align: left; padding-left: 20px;">
                    <li>🌐 Multilingual support (Russian and English)</li>
                    <li>🔔 View unanswered messages</li>
                    <li>✉️ Reply to specific messages</li>
                    <li>📜 View full message history with pagination</li>
                </ul>
            </div>
        </td>
    </tr>
</table>

</div>

---

## 🛠 Technologies

<div align="center">

<table>
    <tr>
        <th>Component</th>
        <th>Version</th>
        <th>Description</th>
        <th>Badge</th>
    </tr>
    <tr align="center">
        <td>Python</td>
        <td>3.10+</td>
        <td>Main development language</td>
        <td><img src="https://img.shields.io/badge/Python-310%2B-3776ABlogo=pythonlogoColor=white" alt="Python"></td>
    </tr>
    <tr align="center">
        <td>python-telegram-bot</td>
        <td>20.0+</td>
        <td>API for Telegram integration</td>
        <td><img src="https://img.shields.io/badge/Telegram%20Bot-20.0%2B-26A5E4?logo=telegram&logoColor=white" alt="Telegram Bot"></td>
    </tr>
    <tr align="center">
        <td>SQLite3</td>
        <td>-</td>
        <td>Data storage</td>
        <td><img src="https://img.shields.io/badge/SQLite3-✓-003B57?logo=sqlite&logoColor=white" alt="SQLite3"></td>
    </tr>
    <tr align="center">
        <td>Logging</td>
        <td>-</td>
        <td>Standard logging module</td>
        <td><img src="https://img.shields.io/badge/Logging-✓-000000?logo=logging&logoColor=white" alt="Logging"></td>
    </tr>
    <tr align="center">
        <td>Architecture</td>
        <td>-</td>
        <td>Fully asynchronous</td>
        <td><img src="https://img.shields.io/badge/Asynchronous-✓-FF6B6B?logo=asynclogoColor=white" alt="Asynchronous"></td>
    </tr>
</table>

</div>

---

## 🔐 Installation and Setup

### 📋 Requirements

<div align="center">

<table>
    <tr align="center">
        <th>Requirement</th>
        <th>Description</th>
        <th>Badge</th>
    </tr>
    <tr align="center">
        <td>Python</td>
        <td>Version 3.10 or newer</td>
        <td><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python"></td>
    </tr>
    <tr align="center">
        <td>Telegram</td>
        <td>Telegram account</td>
        <td><img src="https://img.shields.io/badge/Telegram-✓-26A5E4?logo=telegram&logoColor=white" alt="Telegram"></td>
    </tr>
    <tr align="center">
        <td>BotFather</td>
        <td>Bot created via @BotFather</td>
        <td><img src="https://img.shields.io/badge/BotFather-✓-26A5E4?logo=telegram&logoColor=white" alt="BotFather"></td>
    </tr>
</table>

</div>

### 🔍 Getting Telegram ID
1. Find @userinfobot in Telegram
2. Send him the `/start` command
3. The bot will reply with your ID (a number like `123456789`)

### 🔑 Getting Bot Token
1. Open @BotFather in Telegram
2. Use the `/newbot` command to create a new bot
3. After creation, get the token (looks like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### ⚙️ Configuration Setup
Open the `config.py` file and replace the following values at the beginning of the file:

```python
# Your personal admin ID (received from @userinfobot)
YOUR_CHAT_ID = '!!!⚠️ your chat id ⚠️!!!'  # Replace with your ID

# Your bot token (received from @BotFather)
TELEGRAM_BOT_TOKEN = '!!!⚠️ your bot token ⚠️!!!'  # Replace with bot token
```

### 📦 Installing Dependencies
```
pip install -r requirements.txt
```

### 🚀 Starting the Bot
```
python main.py
```

---

## 📋 Project Structure

```
telegram-feedback-bot/
├── bot/
│   ├── config.py         # Configuration and localization
│   ├── database.py       # Models and database operations
│   ├── handlers.py       # Message handlers
│   ├── keyboards.py      # Keyboard generation
│   └── main.py           # Main executable file
├── .gitignore            # Git ignored files
├── bot.log               # Log file (created automatically)
├── feedback_bot.db       # Database (created automatically)
├── LICENSE               # Project license
├── README.md             # English documentation
├── README.ru.md          # Russian documentation
└── requirements.txt      # Dependencies
```

---

## 💡 Tips:
- 📊 All messages are saved in the database, even after bot restart
- 🔍 Check bot.log file to view logs
- ⚡ Database and log files are created automatically on first launch

## ⚠️ Important Note
This project was developed by a beginner self-taught programmer. The code may contain:
- ❌ Errors and bugs
- ⚡ Suboptimal solutions
- 🛡️ Architectural shortcomings

---

## 📩 Contacts
I'm open to constructive criticism and suggestions for code improvement. If you found an error or know how to do something better - please contact me!

[![Telegram](https://img.shields.io/badge/-MordaRedFox-0088cc?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/MordaRedFox)
&nbsp;
[![Email](https://img.shields.io/badge/-mordaredfox@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:mordaredfox@gmail.com)
