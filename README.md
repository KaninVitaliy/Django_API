# API документация
Этот проект представляет собой RESTful API, разработанный с использованием Django и Django REST Framework. Он позволяет пользователям выполнять CRUD (создание, чтение, обновление и удаление) операции с постами, комментариями и лайками.
## Инструкция к работе над проектом
### Предпосылки

- Python 3.x
- Django
- Django REST Framework
- База данных (PostgreSQL, SQLite)

# 1. Запуск проекта
### 1.1. Клонируйте репозиторий и перейдите в рабочую директорию:
```bash
git clone https://git@github.com:KaninVitaliy/Django_API.git
cd social_network
```
### 1.2. Установите зависимости из файла `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 1.3. Создайте виртуальное окружение для проекта:

```bash
python -m venv env
```

Активируйте виртуальное окружение:

- **Для Windows:**

  ```bash
  .\env\Scripts\activate
  ```

- **Для macOS/Linux:**

  ```bash
  source env/bin/activate
  ```


### 1.4. Настройка базы данных 

Создайте базу данных, выполнив команду в терминале:

```commandline
createdb -U postgres <имя бд> 
```

В файле settings.py настройте конфигурацию для вашей базы данных
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<имя бд>',
        'USER': 'ваше имя',
        'PASSWORD': 'ваш пароль',
        'HOST': 'localhost',
        'PORT': 5432
    }
}
```
### 1.5. Примените необходимые миграции

```commandline
python manage.py migrate
```
### 1.6. Создайте пользователя для получения токена.

```commandline
python manage.py createsuperuser
```
### 1.7. Запустите сервер 

```commandline
python manage.py runserver
```

#### Cервер будет доступен по адресу :
```python
http://127.0.0.1:8000/
```

# 2. Аутентификация
### API использует токен-авторизацию. Для получения токена аутентификации зайдите в административную панель и создайте токен 

Адрес где получить токен: 
``` commandline
http://127.0.0.1:8000/admin/authtoken/tokenproxy/
```

# 3 Запросы CRUD
####  Все запросы вы можете выполнить из файла `requests-examples.http` либо через программу Postman
### 3.1 Работа с постами

#### Чтобы получить список всех постов, отправьте GET запрос на адрес из примера:
(запрос на получение всех постов вы можете выполнить без аутентификации)

``` commandline
GET http://127.0.0.1:8000/api/posts/
```

#### Создать новый пост
###### Пример запроса на создание поста с локацией
```text
POST http://127.0.0.1:8000/api/posts/
Authorization: Token your_token_here
Content-Type: application/json

{
  "text": "Test Post",
  "location": "Moscow,Russia",
  "images": (file)
}
```

#### Получить конкретный пост

```text
GET http://127.0.0.1:8000/api/posts/{post_id}
```

#### Обновить пост

```text
PUT http://127.0.0.1:8000/api/posts/{post_id}/
Authorization: Token your_token_here
Content-Type: application/json

{
    "title": "Новое название поста",
    "content": "Обновлённое содержимое поста"
}
```

#### Удалить пост

```text
DELETE http://127.0.0.1:8000/api/posts/{post_id}
Authorization: Token your_token_here
```

### 3.2. Комментарии

#### Получить список комментариев к посту

```text
GET http://127.0.0.1:8000/api/posts/{post_id}/comments/
```

#### Добавить комментарий к посту

```text
POST http://127.0.0.1:8000/api/posts/{post_id}/comments/
Authorization: Token your_token_here
Content-Type: application/json

{
  "author": 1,
  "text": "Отличный пост!"
}
```

#### Удалить комментарий

```text
DELETE http://127.0.0.1:8000/api/posts/{post_id}/comments/
Authorization: Token your_token_here
```
### 3.3 Лайки
Поставить и убрать лайк можно одним и тем же запросом:
```text
POST http://127.0.0.1:8000/api/posts/1/likes
Content-Type: application/json
Authorization: Token your_token_here
```

# Заключение

Данная документация описывает основные функции, доступные в вашем API. За дополнительной информацией обращайтесь к коду проекта или задавайте вопросы разработчику.





