#Django Test Task

##Установка и Настройка

###Для проекта необходимы пакеты
```
* Nginx
* supervisor (require Python)
* PostgreSQL 9.x
* Python 2.7.9
* Git
* nodejs
* npm
* bower
```
###Копирование:
```
git clone https://github.com/jackfrodo/test_task
cd test_task
```
###Установка пакетов (основные):
```
pip install django
pip install django-filter
pip install django-bower
pip install psycopg2
pip install gunicorn
```
###Установка зависомостей:
```
python manager.py bower install
```
###Создание база данных
```
Создать "db_employees" в PostgreSQL:
Прописать настройки подключения DATABASES в test_task/settings.py
```
###Провести миграцию
```
python manage.py migrate
```
###Создать суперпользователя
```
python manage.py createsuperuser
```
###Запустить сервер
```
python manage.py runserver
запуститься локально, если нужен bind на другой ip:
python manage.py runserver 0.0.0.0:8000 (на все сетевый интерфейсы и порт 8000)
```
###Future
```
Есть скрипт fabfile с fabric, не полный, нужна доработка. Mожно попробовать запустить для автоматической установка, но только локально
```
