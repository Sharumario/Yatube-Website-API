# Проект «Yatube website + API Yatube».
### Описание API
API для Yatub представляет собой проект социальной сети в которой реализованы следующие возможности, 
публиковать посты, комментировать посты, а так же подписываться или отписываться от авторов.
### Технологии
![Python](https://img.shields.io/badge/Python-3.9.8-%23254F72?style=flat-square&logo=python&logoColor=yellow&labelColor=254f72)
![Django](https://img.shields.io/badge/Django-2.2.16-0C4B33?style=flat-square&logo=django&logoColor=white&labelColor=0C4B33)
![Django](https://img.shields.io/badge/Django%20REST-3.12.4-802D2D?style=flat-square&logo=django&logoColor=white&labelColor=802D2D)
![Django](https://img.shields.io/badge/JWT+Djoser-50c878?style=flat-square&logo=jwt)
### Возможности проекта:
- Публикация записей с изображениями.
- Публикация записей в сообщества.
- Комментарии к записям других авторов.
- Подписка на других авторов.
- Лента с записями, на которых оформлена подписка.
- Template tags, отображающие самые обсуждаемые записи, последние записи и пр.
- Для проекта написаны тесты Unittest.
### Возможности API:
- Получение, создание, обновление, удаление записей.
- Получение, создание, обновление, удаление комментариев.
- Получение списка сообществ и их информации.
- Получение списка подписок и создание подписки на авторов.
- Получение, обновление и проверка токена авторизации (JWT).
### Запуск проекта в dev-режиме
- Клонировать репозиторий и перейти в него в командной строке.
- Установите и активируйте виртуальное окружение c учетом версии Python 3.7 (выбираем python не ниже 3.7):
```bash
py -3.7 -m venv venv
venv/Scripts/activate
python -m pip install --upgrade pip
```
- Затем нужно установить все зависимости из файла requirements.txt
```bash
pip install -r requirements.txt
```
- Выполняем миграции:
```bash
python manage.py migrate
```
Создаем суперпользователя:
```bash
python manage.py createsuperuser
```
Запускаем проект:
```bash
python manage.py runserver
```
### Примеры работы с API
Для неавторизованных пользователей работа с API доступна только в режиме чтения(GET-запросы)
```bash
GET api/v1/posts/ - получить список всех публикаций.
При указании параметров limit и offset выдача должна работать с пагинацией
GET api/v1/posts/{id}/ - получение поста по id

GET api/v1/groups/ - получение списка доступных групп
GET api/v1/groups/{id}/ - получение информации о группе по id

GET api/v1/{post_id}/comments/ - получение всех комментариев к посту
GET api/v1/{post_id}/comments/{id}/ - Получение комментария к посту по id
```
### Примеры работы с API для авторизованных пользователей
Для авторизованных пользователей помимо GET запросов, доступны POST, PUT, PATCH, DELETE запросы.
Примеры приведены ниже.
Для создания поста используем:
```bash
POST /api/v1/posts/
```
в body
{
"text": "string",
"image": "string",
"group": 0
}

Обновление поста:
```bash
PUT /api/v1/posts/{id}/
```
в body
{
"text": "string",
"image": "string",
"group": 0
}

Частичное обновление поста:
```bash
PATCH /api/v1/posts/{id}/
```
в body
{
"text": "string",
"image": "string",
"group": 0
}

Удаление поста:
```bash
DEL /api/v1/posts/{id}/
```
Получение доступа к эндпоинту /api/v1/follow/
```bash
GET /api/v1/follow/ - подписка пользователя от имени которого сделан запрос
на пользователя переданного в теле запроса. Анонимные запросы запрещены.
```
- Авторизованные пользователи могут создавать посты,
комментировать их и подписываться на других пользователей.
- Пользователи могут изменять(удалять) контент, автором которого они являются.
### Авторизация по JWT(токену)
Доступ авторизованным пользователем доступен по JWT-токену (Joser),
который можно получить выполнив POST запрос по адресу:
```bash
POST /api/v1/jwt/create/
```
Передав в body данные пользователя (например в postman):
```bash
{
"username": "string",
"password": "string"
}
```
Полученный токен добавляем в headers (postman), после чего буду доступны все функции проекта:
```bash
Authorization: Bearer {your_token}
```
Обновить JWT-токен:
```bash
POST /api/v1/jwt/refresh/ - обновление JWT-токена
```
Проверить JWT-токен:
```bash
POST /api/v1/jwt/verify/ - проверка JWT-токена
```
## Над проектом работали:
[Шайхнисламов Марат](https://github.com/Sharumario/) при поддержке ЯндексПрактикума
