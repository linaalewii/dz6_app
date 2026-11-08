# Учёт заказов кофейни (ДЗ 6)

Сервис учёта заказов кофейни на FastAPI. Код разделён на три слоя: router, service и repository. Заказы хранятся в памяти процесса.

## Бизнес-правило

Заказ в статусе `completed` нельзя ни изменить (`PATCH`), ни отменить (`DELETE`). В обоих случаях сервис вернёт `409 Conflict`. Если заказа с таким id нет, вернётся `404 Not Found`.

## Структура проекта

```
app/
├── main.py          # приложение, роутер и обработчики ошибок
├── config.py        # Settings, get_settings
├── exceptions.py    # OrderNotFoundError, OrderAlreadyCompletedError
├── dependencies.py  # get_repository, get_service, ServiceDep, SettingsDep
├── schemas.py       # модели и перечисления
├── repository.py    # OrderRepository: хранение данных
├── service.py       # OrderService: бизнес-логика
└── routers/
    └── orders.py    # HTTP-эндпоинты заказов
```

## Запуск

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (на Mac/Linux: source .venv/bin/activate)
pip install "fastapi[standard]" pydantic-settings
cp .env.example .env          # по желанию, на Windows: copy .env.example .env
fastapi dev app/main.py
```

Документация API: http://127.0.0.1:8000/docs

## Настройки (`.env`)

| Переменная | По умолчанию | Описание |
|---|---|---|
| `APP_NAME` | Учёт заказов кофейни | Название сервиса |
| `DEFAULT_PAGE_SIZE` | 10 | Размер страницы списка по умолчанию |
| `MAX_PAGE_SIZE` | 50 | Максимальный размер страницы |
