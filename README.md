# «Продуктовый помощник»
[Ссылка на сайт](http://84.252.143.37/)

## Описание
Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
## Технологии
Python 3.8

django 3.2.1

djangorestframework 3.12.4

PostgreSQL

Docker

Nginx

Gunicorn

## Запуск
Пересборка и запуск контейнеров
```bash
docker-compose up -d --build
```

Создание суперюзера
```bash
docker-compose exec web python manage.py createsuperuser
```

Заполнение базы данных начальными данными
```bash
docker-compose exec web python manage.py dumpdata > fixtures.json
```

Клонирование репозитория
```bash
git clone https://github.com/DIKuznetsov/foodgram-project.git
```

[Инструкция по установке docker](https://docs.docker.com/engine/install/ubuntu/)

##Автор проекта:

[Кузнецов Дмитрий](https://github.com/DIKuznetsov)