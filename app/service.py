from .config import Settings, get_settings
from .exceptions import OrderAlreadyCompletedError, OrderNotFoundError
from .repository import OrderRepository
from .schemas import Order, OrderCreate, OrderStatus, OrderUpdate, SortBy


class OrderService:
    def __init__(self, repository: OrderRepository, settings: Settings | None = None):
        self.repository = repository
        self.settings = settings or get_settings()

    def _get_or_raise(self, order_id: int) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        return order

    def _ensure_not_completed(self, order: Order) -> None:
        if order.status == OrderStatus.completed:
            raise OrderAlreadyCompletedError(order.id)

    def count_orders(self) -> int:
        return len(self.repository.get_all())

    def list_orders(
        self,
        order_status: OrderStatus | None = None,
        limit: int | None = None,
        offset: int = 0,
        sort_by: SortBy | None = None,
    ) -> list[Order]:
        result = self.repository.get_all()

        if order_status is not None:
            result = [o for o in result if o.status == order_status]

        if sort_by == SortBy.created_at:
            result.sort(key=lambda o: o.created_at)
        elif sort_by == SortBy.drink:
            result.sort(key=lambda o: o.drink.lower())

        page_size = limit if limit is not None else self.settings.default_page_size
        page_size = min(page_size, self.settings.max_page_size)
        return result[offset : offset + page_size]

    def get_order(self, order_id: int) -> Order:
        return self._get_or_raise(order_id)

    def create_order(self, data: OrderCreate) -> Order:
        order = Order(
            id=self.repository.next_id(),
            status=OrderStatus.pending,
            **data.model_dump(),
        )
        return self.repository.add(order)

    def update_order(self, order_id: int, data: OrderUpdate) -> Order:
        order = self._get_or_raise(order_id)
        self._ensure_not_completed(order)

        changes = {
            key: value
            for key, value in data.model_dump(exclude_unset=True).items()
            if value is not None
        }
        return self.repository.update(order_id, changes)

    def cancel_order(self, order_id: int) -> None:
        order = self._get_or_raise(order_id)
        self._ensure_not_completed(order)
        self.repository.delete(order_id)