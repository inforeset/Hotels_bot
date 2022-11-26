# Hotels Bot
Это простой телеграм бот, 
с помощью него можно получать информацию об отелях, расположенных по всему миру,
в работе использует Rapid Api.

## Used technology
* Python (3.10);
* PyTelegramBotApi (Telegram Bot framework);
* Docker and Docker Compose (containerization);
* PostgreSQL (database);
* Redis (persistent storage for some ongoing data);
* SQLAlchemy (working with database from Python);
* Alembic (database migrations made easy);
* Docker images are built with buildx for both amd64 and arm64 architectures.

## Installation

### Используя докер:
Создайте новый каталог, внутри него сделайте 3 директории для данных бота:
`mkdir -p {pg-data,redis-data,redis-config}`

Скопируйте файл `docker-compose.yml` в ваш новый каталог, рядом с созданными выше директориями:

Скопируйте файл `redis.conf` в `redis-config`. Можете изменить его при необходимости.

Скопируйте файл `.env.template` рядом в каталог рядом с `docker-compose.yml` и переименуйте его в `.env`.
Откройте его и заполните необходимыми данными.

Наконец, запустите вашего бота командой `docker-compose up -d`.


### Обычный режим:
Необходимо скопировать все содержимое репозитария в отдельный каталог.

Установить все библиотеки из `requirements.txt`

Необходимо установить и запустить Postgre сервер, необходимо создать базу данных для использования ботом.

Файл `.env.template` переименуйте в `.env`. Откройте его и заполните необходимыми данными, не забудьте указать
данные для подключения к БД.

Необходимо сделать миграции с помощью команды в консоли `alembic upgrade head`

Необходимо установить и запустить Redis сервер, если предполагается использование Redis.

Запустите файл `__main__.py`.

# Hotels Bot
This is simple telegram bot,
can be used for getting information about hotels around world,
work with Rapid Api.

## Used technology
* Python (3.10);
* PyTelegramBotApi (Telegram Bot framework);
* Docker and Docker Compose (containerization);
* PostgreSQL (database);
* Redis (persistent storage for some ongoing data);
* SQLAlchemy (working with database from Python);
* Alembic (database migrations made easy);
* Docker images are built with buildx for both amd64 and arm64 architectures.

## Installation

### Use Docker:
Create a directory of your choice. Inside it, make 3 directories for bot's data:  
`mkdir -p {pg-data,redis-data,redis-config}`

Grab `docker-compose.yml` and put it next to your directories.

Grab `redis.conf` and put into `redis-config` directory. Change its values for your preference.

Grab `.env.template` file, rename it to `.env` and put it next to your `docker-compose.yml`, open 
and fill the necessary data.

Finally, start your bot with `docker-compose up -d` command.

### Usual mode:
You have to copy all content from repository to the new catalog, inside it make 3 directories for bot's data:  
`mkdir -p {pg-data,redis-data,redis-config}` 

Grab `redis.conf` and put into `redis-config` directory. Change its values for your preference.

Install all packages from `requirements.txt`

You have to install and run Postgre server, and you have to create a database for bot's data.

File `.env.template` rename to `.env`. Open it and fill the necessary data. Don't forget fill data 
for connecting to database.

Make a migrations with `alembic upgrade head` command

You have to install and run Redis server, if it is assumed to use.

Run `__main__.py`.