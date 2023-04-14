FROM python:3.8
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean

# create work dir
RUN mkdir /app
# устанавливаем рабочую директорию
WORKDIR /app


# устанавливаем переменную окружения для проекта
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# копируем зависимости из файла requirements.txt
COPY ./requirements.txt .

# устанавливаем зависимости
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов проекта в образ
COPY . /app/

# Сборка статических файлов
RUN python manage.py collectstatic --noinput