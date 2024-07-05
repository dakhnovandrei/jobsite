# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# Создаем рабочую директорию
WORKDIR /pythonProject7

# Копируем файлы проекта в контейнер
COPY . /pythonProject7

# Устанавливаем виртуальное окружение
RUN python -m venv /pythonProject7/.venv

# Активируем виртуальное окружение и устанавливаем зависимости
RUN /bin/bash -c "source /pythonProject7/.venv/Scripts/activate && pip install --upgrade pip && pip install -r /pythonProject7/jobsite/requirements.txt"

# Указываем переменную окружения для настройки Django
ENV DJANGO_SETTINGS_MODULE=jobsite.settings

# Открываем порт 8000
EXPOSE 8000

# Выполняем миграции и запускаем сервер
CMD /bin/bash -c "source /pythonProject7/.venv/Scripts/activate && python /pythonProject7/jobsite/manage.py migrate && python /pythonProject7/jobsite/manage.py runserver 0.0.0.0:8000"