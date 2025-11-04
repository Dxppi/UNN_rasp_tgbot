# 🎓 UNN Schedule Telegram Bot

[English](#english) | [Русский](#русский)

---

<a name="русский"></a>
## Русский

Telegram бот для получения расписания занятий ННГУ. Бот использует HTTP запросы через `urllib.request`, реализует диспетчер с поддержкой состояний и сохраняет данные пользователей в SQLite.

### 🚀 Быстрый старт

#### 1. Клонирование репозитория

```bash
git clone https://github.com/Dxppi/UNN_rasp_tgbot.git
cd UNN_rasp_tgbot
```

#### 2. Создание виртуального окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

#### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
TOKEN=your_telegram_bot_token
DB_PATH=database.sqlite
```

Где:
- `TOKEN` - токен вашего Telegram бота (получите у [@BotFather](https://t.me/BotFather))
- `DB_PATH` - путь к файлу базы данных (по умолчанию: `database.sqlite`)

#### 5. Запуск бота

```bash
python -m bot
```

### 🐳 Запуск через Docker

#### Запуск контейнера

```bash
docker-compose up -d
```

База данных будет сохраняться в директории `./data` на вашем компьютере.

### 📱 Использование бота

#### Команды

- `/start` - запустить бота (восстанавливает сохраненную группу или просит ввести новую)
- `/change` - изменить номер группы
- `/today` - расписание на сегодня
- `/tomorrow` - расписание на завтра
- `/week` - расписание на неделю
- `/cancel` - отменить текущую операцию
- `/help` - показать справку (доступна через кнопку "Помощь")

#### Кнопки клавиатуры

- **Сегодня** - получить расписание на сегодня
- **Завтра** - получить расписание на завтра
- **Неделя** - получить расписание на неделю
- **Помощь** - показать справку по командам

### 💾 База данных

#### Структура базы данных

Бот использует SQLite для хранения данных пользователей. База данных автоматически создается при первом запуске.

**Таблица: `user_groups`**

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | INTEGER | Первичный ключ |
| `user_id` | INTEGER UNIQUE NOT NULL | Telegram ID пользователя |
| `group_number` | TEXT NOT NULL | Номер группы (например, "3822Б1ФИ2) |
| `group_id` | TEXT NOT NULL | Внутренний ID группы из API ННГУ |

#### Пример запросов

Просмотр всех сохраненных пользователей:
```sql
SELECT user_id, group_number, group_id FROM user_groups;
```

Просмотр группы конкретного пользователя:
```sql
SELECT group_number, group_id FROM user_groups WHERE user_id = 123456789;
```

#### Архитектура базы данных

Проект использует паттерн **Repository** с интерфейсом `DatabaseInterface`:

- `db/database_interface.py` - абстрактный интерфейс для работы с БД
- `db/sqlite_database.py` - реализация для SQLite

Это позволяет легко заменить SQLite на другую БД или использовать моки для тестирования.

### 📁 Структура проекта

```
UNN_rasp_tgbot/
├── bot/                    # Основной код бота
│   ├── handlers/          # Обработчики команд и сообщений
│   ├── dispatcher.py      # Диспетчер с поддержкой состояний
│   ├── telegram_api.py    # HTTP клиент для Telegram API
│   ├── longpolling.py     # Long Polling механизм
│   └── config.py          # Конфигурация
├── db/                     # Работа с базой данных
│   ├── database_interface.py  # Интерфейс БД
│   └── sqlite_database.py     # Реализация SQLite
├── parser/                 # Парсинг расписания
│   └── parseData.py       # Получение данных из API ННГУ
├── data/                   # Директория для базы данных (создается автоматически)
├── .env                    # Переменные окружения
├── requirements.txt        # Зависимости Python
├── Dockerfile             # Конфигурация Docker
└── README.md             # Документация
```

---

<a name="english"></a>
## English

Telegram bot for getting NNSU (UNN) class schedules. The bot uses HTTP requests via `urllib.request`, implements a dispatcher with state management, and stores user data in SQLite.

### 🚀 Quick Start

#### 1. Clone Repository

```bash
git clone https://github.com/Dxppi/UNN_rasp_tgbot.git
cd UNN_rasp_tgbot
```

#### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Setup Environment Variables

Create `.env` file in the project root:

```env
TOKEN=your_telegram_bot_token
DB_PATH=database.sqlite
```

Where:
- `TOKEN` - your Telegram bot token (get it from [@BotFather](https://t.me/BotFather))
- `DB_PATH` - path to database file (default: `database.sqlite`)

#### 5. Run Bot

```bash
python -m bot
```

### 🐳 Running with Docker

```bash
docker-compose up -d
```

Database will be saved in `./data` directory on your computer.

### 📱 Using the Bot

#### Commands

- `/start` - start the bot (restores saved group or asks to enter new one)
- `/change` - change group number
- `/today` - schedule for today
- `/tomorrow` - schedule for tomorrow
- `/week` - schedule for the week
- `/cancel` - cancel current operation
- `/help` - show help (available via "Помощь" button)

#### Keyboard Buttons

- **Сегодня** (Today) - get today's schedule
- **Завтра** (Tomorrow) - get tomorrow's schedule
- **Неделя** (Week) - get week's schedule
- **Помощь** (Help) - show command reference

### 💾 Database

#### Database Structure

The bot uses SQLite to store user data. Database is automatically created on first run.

**Table: `user_groups`**

| Field | Type | Description |
|-------|------|-------------|
| `id` | INTEGER | Primary key |
| `user_id` | INTEGER UNIQUE NOT NULL | Telegram user ID |
| `group_number` | TEXT NOT NULL | Group number (e.g., "3822Б1ФИ2") |
| `group_id` | TEXT NOT NULL | Internal group ID from NNSU API |

#### Example Queries

View all saved users:
```sql
SELECT user_id, group_number, group_id FROM user_groups;
```

View specific user's group:
```sql
SELECT group_number, group_id FROM user_groups WHERE user_id = 123456789;
```

#### Database Architecture

The project uses **Repository pattern** with `DatabaseInterface`:

- `db/database_interface.py` - abstract interface for database operations
- `db/sqlite_database.py` - SQLite implementation

This allows easy replacement of SQLite with another database or using mocks for testing.

### 📁 Project Structure

```
UNN_rasp_tgbot/
├── bot/                    # Main bot code
│   ├── handlers/          # Command and message handlers
│   ├── dispatcher.py      # Dispatcher with state management
│   ├── telegram_api.py    # HTTP client for Telegram API
│   ├── longpolling.py     # Long Polling mechanism
│   └── config.py          # Configuration
├── db/                     # Database layer
│   ├── database_interface.py  # Database interface
│   └── sqlite_database.py     # SQLite implementation
├── parser/                 # Schedule parsing
│   └── parseData.py       # Fetching data from NNSU API
├── data/                   # Database directory (created automatically)
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
└── README.md             # Documentation
```
