## Birthday reminder

Данный сервис предоставляет возможность элегантно и оригинально поздравлять ваших клиентов, а также эффективно
распространять коммерческие предложения через популярную платформу Telegram. Мы считаем, что важно придавать
значимость каждому моменту общения с вашей аудиторией

### Стек технологий

- Python
- Django
- - ---------------
Bootstrap
- ---------------

- PostgresSQL

- - ---------------

- Pyrogram

- - ---------------

- Celery
- Radis
- Schedule

- - ---------------

- Docker
- Jinja2
- Nginx

---

### Установка

Перед запуском проекта убедитесь, что у вас установлен python, docker и docker-compose.

```bash
python --version
```

```
docker --version
```

```
docker-compose --version
```

Создаём .env файл и добавляем следующие настройки

- Настройки сервера
    - `DJANGO_ALLOWED_HOSTS=`...(Добавить свой Хост: "DJANGO_ALLOWED_HOSTS=localhost 80.78.248.167 [::1]")
    - `DEBUG=`... (поумолчанию False)
    - `SECRET_KEY=`... (обязательное поле)

- Настройки базы данных
    - `POSTGRES_HOST=`... (Если запускаем через докер то "db")
    - `POSTGRES_PORT=`... (поумолчанию 5432)
    - `POSTGRES_DB=`... (обязательное поле)
    - `POSTGRES_USER=`... (обязательное поле)
    - `POSTGRES_PASSWORD=`... (обязательное поле)

- Настройка Celery
    - `CELERY_BROKER_URL=`... (обязательное поле. Если запускаем через докер то "redis://redis:6379")
    - `CELERY_RESULT_BACKEND=`... (обязательное поле. Если запускаем через докер то "redis://redis:6379")


- Pyrogram
    - `API_ID=`... (обязательное поле)
    - `API_HASH=`... (обязательное поле)
    - `SESSIONS_FOLDER=`... (обязательное поле. Если запускаем через докер то "
      /home/app/telegram_bot/my_session/account"
      )

## Для настройки сессии user_bot-a " перейдите в директорию telegram_bot"

откройте скрипт под названием **get_session** и в самом низу пропишите **# asyncio.run(get_string_session())**

Затем запустите скрипт и укажите свой контакт (после проделанных действий, не забудьте удалить добавленную
строку)

```
python get_session.py
```

Запускаем проект, перейдя в корень проекта используя команду

```
sudo docker-compose up
```

## Запуск на локальной машине

### настраиваем .env

Устанавливаем зависимости

```
python manage.py -r requirements.txt
```

Запускаем Radis

```
docker run -d -p 6379:6379 redis
```

проверка работы radis-a

```
docker exec -it redis-server redis-cli
```

Устанавливаем Celery, для этого перейдите по ссылке
**https://django.fun/ru/docs/celery/5.1/getting-started/first-steps-with-celery/**

Запускаем Celery

```
python -m celery -A reminder_service worker  --loglevel=INFO

```

Запускаем проект

```
python manage.py runserver 
```

# На этом настройка проекта завершена, Если что-то не работает, то всегда рад помочь. Мой телеграмм @Razzakov_Timur
