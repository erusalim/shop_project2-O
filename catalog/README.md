# Интернет-магазин (Django)

## Требования

- Python 3.10+
- PostgreSQL (опционально; если не настроен — используется SQLite)

## Запуск проекта

### 1. Клонирование и окружение

```bash
cd shop_project
python -m venv venv
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (cmd) / Linux / macOS:**
```bash
# Windows cmd
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Переменные окружения

Скопируйте пример и при необходимости отредактируйте:

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS
```

В `.env` задайте свой `SECRET_KEY`. Для работы с PostgreSQL укажите `DB_NAME`, `DB_USER`, `DB_PASSWORD`.  
Если **PostgreSQL ещё не настроен**, закомментируйте или удалите строку `DB_NAME=shop` в `.env` — тогда будет использоваться SQLite.

### 4. База данных PostgreSQL (если используете)

В psql от пользователя с правами создания БД:

```sql
CREATE USER shop_user WITH PASSWORD 'StrongPass123';
CREATE DATABASE shop OWNER shop_user;
```

Затем выполните миграции (см. ниже).

### 5. Миграции

```bash
python manage.py migrate
```

### 6. Суперпользователь (админка)

```bash
python manage.py createsuperuser
```

Логин для входа в админку указывается при создании. Пароль можно сообщить преподавателю отдельно.

### 7. Запуск сервера

```bash
python manage.py runserver
```

Откройте в браузере:

- Сайт: http://127.0.0.1:8000/
- Админка: http://127.0.0.1:8000/admin/

## Основные команды

| Команда | Описание |
|--------|----------|
| `python manage.py runserver` | Запуск сервера |
| `python manage.py migrate` | Применить миграции |
| `python manage.py makemigrations` | Создать миграции после изменения моделей |
| `python manage.py createsuperuser` | Создать учётную запись администратора |

## Структура приложений

- **catalog** — каталог: категории, товары, изображения товаров
- **orders** — заказы и позиции заказов
- **accounts** — учётные записи (заготовка)

## Тестовые данные

После входа в админку (/admin):

1. Добавьте не менее 3 категорий.
2. Добавьте не менее 10 товаров и привяжите их к категориям.
3. При наличии модели изображений — добавьте картинки минимум к 3 товарам.

## Данные администратора

- **Логин:** задаётся при `createsuperuser` (например, `admin`).
- **Пароль:** задаётся при `createsuperuser`; при сдаче проекта пароль можно сообщить преподавателю отдельно.