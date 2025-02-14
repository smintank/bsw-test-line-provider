# Bet-Maker

## Описание
**Bet-Maker** — это сервис для управления ставками, позволяющий:
- Делать ставки на события
- Просматривать историю ставок
- Получать информацию о текущих событиях

Проект использует **FastAPI**, **PostgreSQL** и **Docker Compose**.

## Запуск проекта

### 1. Подготовка
Создайте файл `.env` в корневой директории проекта и добавьте в него:
```
DEBUG=False

BET_MAKER_HOST=0.0.0.0
BET_MAKER_PORT=8000

LINE_PROVIDER_HOST=0.0.0.0
LINE_PROVIDER_PORT=8080

NGINX_HOST_PORT=8000

POSTGRES_USER=<your_postgres_user>
POSTGRES_PASSWORD=<your_postgres_password>
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=<your_postgres_db>
```

### 2. Запуск через Docker Compose
```sh
docker-compose up --build
```

После этого сервис будет доступен по адресу `http://localhost:8000`.

### 3. Запуск локально (без Docker)
#### Установка зависимостей
```sh
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r bet-maker/requirements.txt
```

#### Запуск FastAPI
```sh
cd bet-maker
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

Если у вас возникли вопросы или проблемы с запуском, создайте issue или свяжитесь с разработчиком.


