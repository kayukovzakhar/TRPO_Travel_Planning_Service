# Travel Planning Service Backend

Backend часть сервиса для планирования путешествий, разработанная с использованием FastAPI и PostgreSQL.

## Функциональность

- Аутентификация пользователей
- Управление местами (добавление, редактирование, удаление)
- Поиск мест по категориям и тегам
- Поиск ближайших мест по координатам
- Управление маршрутами
- Чек-листы для путешествий

## Технологии

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv .venv
```

2. Активируйте виртуальное окружение:
```bash
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте базу данных PostgreSQL и обновите файл `.env` с вашими учетными данными

5. Запустите приложение:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Документация

После запуска приложения документация API будет доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 