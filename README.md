# **Bet-Maker**

## **Описание**
**Bet-Maker** — это сервис для управления ставками, позволяющий:

- Делать ставки на события
- Просматривать историю ставок
- Получать информацию о текущих событиях
- Обновлять статус событий в режиме реального времени через интеграцию с `RabbitMQ`

Проект использует **FastAPI, PostgreSQL, RabbitMQ и Docker Compose**.

---

## **Запуск проекта**

### **1. Подготовка**
Создайте файл `.env` в корневой директории проекта и добавьте в него:

```ini
# Основные настройки
DEBUG=False

# Настройки сервиса ставок
BET_MAKER_HOST=0.0.0.0
BET_MAKER_PORT=8000

# Настройки провайдера событий
LINE_PROVIDER_HOST=0.0.0.0
LINE_PROVIDER_PORT=8080

# Настройки Nginx
NGINX_HOST_PORT=8000

# PostgreSQL
POSTGRES_USER=<your_postgres_user>
POSTGRES_PASSWORD=<your_postgres_password>
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=<your_postgres_db>

# RabbitMQ
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=user
RABBITMQ_PASSWORD=password
RABBITMQ_QUEUE=event_updates
```

---

### **2. Запуск через Docker Compose**
```sh
docker-compose up --build
```
После этого сервис будет доступен по адресу:  
📍 **[http://localhost:8000](http://localhost:8000)**

---

### **3. Запуск локально (без Docker)**

#### **Установка зависимостей**
```sh
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r bet-maker/requirements.txt
```

#### **Запуск FastAPI**
```sh
cd bet-maker
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### **Запуск RabbitMQ-консьюмера**
```sh
cd bet-maker
python services/rabbitmq_consumer.py
```

---

## **API эндпоинты**

### **1. Ставки**
- `POST /bet/` — создание ставки
- `GET /bets/` — получение истории ставок

### **2. События**
- `GET /events/{event_id}/` — получение информации о событии
- `PATCH /events/{event_id}/` — обновление статуса события

