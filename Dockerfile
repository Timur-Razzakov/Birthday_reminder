FROM python:3.8



# устанавливаем переменную окружения для проекта
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean

# копируем зависимости из файла requirements.txt
COPY ./requirements.txt .
# устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade pip



# Копирование файлов проекта в образ
COPY . /app

# устанавливаем рабочую директорию
WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

