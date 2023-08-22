# Практика 2023 Коротков Егор А-01-20

## Создание виртуального окружения

```
python -m venv venv
```

Сразу же запустите его командой:

Если ОС Windows:

```
source venv/Scripts/activate
```

Если ОС Linux:

```
. venv/bin/activate
```

## Установка модулей

```
python -r requirements.txt
```

## Создание файла .env

``` 
touch .env
```

Его содержание:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=qwerty
PORT=5432
DB_NAME=practice2023
```

## Запуск docker-container

```
docker-compose up -d --build
```

## Создание таблицы practice2023

Перейдите в командную строку PostgreSQL

```
docker exec -it db psql -U postgres
```

Создайте таблицу 

```
CREATE DATABASE practice2023;
```

## Перенос данных из dump.sql в practice2023

Выйдете из командной строки PostgreSQL и выполните команду

```
docker exec -it db psql -U postgres -d practice2023 -f dump.sql
```

Данные успешно загружены и дальше запускайте код в main.py!

Для остановки контейнера выполните
```
docker-compose down -v 
```