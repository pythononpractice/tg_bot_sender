# Telegram бот с созданием рассылок по базе пользователей от 23.03.2024

Перед запуском необходимо выполнить команду ```pip install -r requirements.txt```

Для работы необходимо создать файл .env в корне проекта:
```
DATABASE_URL=postgresql+asyncpg://username:password@ip:port/db_name
TOKEN=ВАШ ТОКЕН БОТА
ADMIN_IDS=id пользователей, кто сможет пользоваться командой /sender (например 1111111,2222222)  
```

Для создание таблиц 
```alembic revision --autogenerate -m 'initial'``` и ```alembic upgrade head```
