EVENT_UNAVAILABLE = "Уже нельзя сделать ставку на это событие."
EVENT_NOT_IN_API = "Событие %s не найдено в Line-provider"
EVENT_NOT_EXISTS = "Такого события не существует"

API_JSON_ERROR = "[%s] Ошибка декодирования JSON: %s"
API_HTTP_ERROR = "[%s] Ошибка HTTP: %s"
API_REQUEST_ERROR = "[%s] Ошибка запроса: %s"
API_UNKNOWN_ERROR = "[%s] Непредвиденная ошибка: %s"

RABBITMQ_EVENT_UPDATED = "Обновление ставки для события %s, новый статус: %s"
RABBITMQ_EVENT_NOT_UPDATED = (
    "У события %s не был обновлен статус на: %s, событие не найдено"
)
RABBITMQ_READY_FOR_MSGS = "[*] Ожидание сообщений. Для выхода нажмите CTRL+C"
RABBITMQ_RUN_CONSUMER = "Starting rabbitmq consumer"

DB_ERROR = "Ошибка работы с БД: %s"
