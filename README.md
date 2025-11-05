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
DB_PATH=data/database.sqlite
```

Где:
- `TOKEN` - токен вашего Telegram бота (получите у [@BotFather](https://t.me/BotFather))
- `DB_PATH` - путь к файлу базы данных (по умолчанию: `data/database.sqlite`)

#### 5. Запуск бота

```bash
python -m bot
```

### 🐳 Запуск через Docker

#### 1. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
TOKEN=your_telegram_bot_token
```

> **Примечание:** В Docker переменная `DB_PATH` устанавливается автоматически через `docker-compose.yml` и указывает на `/app/data/database.sqlite`.

#### 2. Запуск контейнера

```bash
docker-compose up -d
```

#### 3. Остановка контейнера

```bash
docker-compose down
```

**Важно:** База данных сохраняется в директории `./data` в корне проекта. Эта папка монтируется в контейнер, поэтому данные сохраняются между перезапусками контейнера.

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
DB_PATH=data/database.sqlite
```

Where:
- `TOKEN` - your Telegram bot token (get it from [@BotFather](https://t.me/BotFather))
- `DB_PATH` - path to database file (default: `data/database.sqlite`)

#### 5. Run Bot

```bash
python -m bot
```

### 🐳 Running with Docker

#### 1. Setup Environment Variables

Create `.env` file in the project root:

```env
TOKEN=your_telegram_bot_token
```

#### 2. Start Container

```bash
docker-compose up -d
```

#### 3. Stop Container

```bash
docker-compose down
```


**Important:** Database is saved in `./data` directory in the project root. This folder is mounted into the container, so data persists between container restarts.

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
