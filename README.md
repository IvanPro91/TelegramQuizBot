# QuizBot Platform

Платформа для создания и проведения викторин в Telegram с аналитикой и статистикой.

## Основные возможности

- 🎯 Создание викторин через интуитивный конструктор
- 📊 Детальная аналитика и статистика ответов
- 🏆 Рейтинг пользователей по результатам
- 🔧 Гибкие настройки викторин
- 📱 Интеграция с Telegram

## Технологии

- **Backend**: Python Django
- **Frontend**: Tabler.IO, Bootstrap 5
- **Database**: PostgreSQL
- **Messaging**: Telegram Bot API

## Установка и запуск

### Установка через Poetry

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/IvanPro91/TelegramQuizBot.git
cd TelegramQuizBot
```

Установите зависимости:

bash
poetry install
Активируйте виртуальное окружение:

bash
poetry shell
Настройте базу данных PostgreSQL:

Установите PostgreSQL:

bash
sudo apt-get install postgresql postgresql-contrib
Создайте базу данных и пользователя:

bash
sudo -u postgres createdb quiz_database
sudo -u postgres createuser --pwprompt quiz_user
Настройте переменные окружения:
Создайте файл .env в корне проекта:

env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgres://quiz_user:yourpassword@localhost:5432/quiz_database
Для SQLite:

env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
Установите зависимости для PostgreSQL:

bash
poetry add psycopg2-binary
Примените миграции:

bash
python manage.py migrate
Создайте суперпользователя:

bash
python manage.py createsuperuser
Запустите сервер разработки:

bash
python manage.py runserver
Команды Poetry
bash
# Установка зависимостей
poetry install

# Добавление пакетов
poetry add package-name
poetry add --dev package-name

# Запуск команд
poetry run python manage.py migrate
poetry run python manage.py runserver

# Активация окружения
poetry shell

# Миграции
poetry run python manage.py makemigrations
poetry run python manage.py migrate

# Резервное копирование
poetry run python manage.py dumpdata > backup.json
poetry run python manage.py loaddata backup.json

# Тестирование
```bash
poetry run python manage.py test
```

# Troubleshooting

## Проблемы с PostgreSQL
Проверьте статус: sudo systemctl status postgresql

Убедитесь в правильности пользователя и пароля

## Проблемы с Poetry
Обновите: poetry self update

Очистите кэш: poetry cache clear --all pypi