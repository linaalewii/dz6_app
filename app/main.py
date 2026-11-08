from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .dependencies import ServiceDep, SettingsDep
from .exceptions import OrderAlreadyCompletedError, OrderNotFoundError
from .routers import orders

TAG_SERVICE = "Сервис"

app = FastAPI(
    title="Учёт заказов кофейни",
    description=(
        "Маленький сервис для бариста: создать заказ, посмотреть список, "
        "отметить готовым или выполненным и отменить.\n\n"
        "Данные хранятся в памяти и пропадают при перезапуске сервера."
    ),
    version="1.0.0",
)

app.include_router(orders.router)


@app.get("/", tags=[TAG_SERVICE], summary="Приветствие сервиса")
def read_root():
    return {"message": "Сервис учёта заказов кофейни на связи"}


@app.get("/info", tags=[TAG_SERVICE], summary="Информация о сервисе")
def get_info(settings: SettingsDep, service: ServiceDep):
    return {"app_name": settings.app_name, "orders_count": service.count_orders()}


@app.exception_handler(OrderNotFoundError)
async def order_not_found_handler(request: Request, exc: OrderNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Заказ с id={exc.order_id} не найден"},
    )


@app.exception_handler(OrderAlreadyCompletedError)
async def order_completed_handler(request: Request, exc: OrderAlreadyCompletedError):
    return JSONResponse(
        status_code=409,
        content={"detail": f"Заказ {exc.order_id} уже выполнен и не может быть изменён"},
    )