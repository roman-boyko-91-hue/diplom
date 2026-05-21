# API для управления библиотекой

Дипломный проект: система для автоматизации работы библиотеки, управления книжным каталогом и отслеживания выдачи книг пользователям.

## Стек технологий
* **Backend**: Python 3.13 / Django 5.0 / Django Rest Framework (DRF)
* **База данных**: PostgreSQL
* **Аутентификация**: JWT (JSON Web Tokens)
* **Документация**: OpenAPI / Swagger UI (`drf-yasg`)
* **Контейнеризация**: Docker / Docker Compose

---

## Структура проекта
* `core/` — Главный модуль настроек проекта (settings, urls).
* `users/` — Управление пользователями, кастомная модель (вход по Email), роли (Библиотекарь/Читатель).
* `authors/` — База данных авторов и управление информацией о них.
* `books/` — Каталог книг с фильтрацией по жанрам и полнотекстовым поиском по автору/названию.
* `loans/` — Модуль выдачи книг, контроль остатков на складе и фиксация возвратов.

---

## Инструкция по локальному запуску

### 1. Клонирование и настройка окружения
```bash
git clone <https://github.com/roman-boyko-91-hue/diplom>
python -m venv .venv
source .venv\Scripts\activate # для Windows
pip install -r requirements.txt
```

### 2. Настройка переменных окружения
Создайте файл `.env` в корневом каталоге проекта по шаблону:
```text
DEBUG=True
SECRET_KEY=your_secret_key
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 3. Миграции и запуск
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
После запуска проект будет доступен по адресу: `http://127.0.0`

---

## Интерактивная документация API
После запуска сервера вам доступны следующие эндпоинты автодокументации:
* **Swagger UI**: `http://127.0.0.8000/swagger/` — интерактивное тестирование всех эндпоинтов (создание книг, авторов, аренда).

---

## Запуск через Docker
Сборка через Docker Compose:
```bash
docker compose up --build
```