from typing import Annotated

from fastapi import APIRouter, Query, Response, status

from ..dependencies import ServiceDep
from ..schemas import Order, OrderCreate, OrderStatus, OrderUpdate, SortBy

router = APIRouter(prefix="/orders", tags=["Заказы"])


@router.post(
    "",
    response_model=Order,
    status_code=status.HTTP_201_CREATED,
    summary="Создать заказ",
)
def create_order(data: OrderCreate, service: ServiceDep):
    return service.create_order(data)


@router.get("", response_model=list[Order], summary="Список заказов")
def list_orders(
    service: ServiceDep,
    order_status: Annotated[
        OrderStatus | None,
        Query(alias="status", description="Фильтр по статусу заказа"),
    ] = None,
    limit: Annotated[
        int | None,
        Query(
            ge=1,
            description=(
                "Сколько заказов вернуть. Если не указано — значение из настроек; "
                "больше максимума из настроек не отдаётся."
            ),
        ),
    ] = None,
    offset: Annotated[
        int, Query(ge=0, description="Сколько заказов пропустить с начала")
    ] = 0,
    sort_by: Annotated[
        SortBy | None,
        Query(description="Сортировка: по времени создания или по названию напитка"),
    ] = None,
):
    return service.list_orders(order_status, limit, offset, sort_by)


@router.get("/{order_id}", response_model=Order, summary="Получить заказ по id")
def get_order(order_id: int, service: ServiceDep):
    return service.get_order(order_id)


@router.patch(
    "/{order_id}", response_model=Order, summary="Частично обновить заказ"
)
def update_order(order_id: int, data: OrderUpdate, service: ServiceDep):
    return service.update_order(order_id, data)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Отменить (удалить) заказ",
)
def cancel_order(order_id: int, service: ServiceDep):
    service.cancel_order(order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)