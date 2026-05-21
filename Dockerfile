FROM python:3.13-slim

# Устанавливаем системные зависимости для компиляции некоторых пакетов Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Открываем порт для Django
EXPOSE 8000

# Запускаем сервер разработки Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
