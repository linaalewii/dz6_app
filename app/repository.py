from .schemas import Order


class OrderRepository:
    def __init__(self):
        self._orders: list[Order] = []
        self._next_id = 1

    def next_id(self) -> int:
        order_id = self._next_id
        self._next_id += 1
        return order_id

    def get_all(self) -> list[Order]:
        return list(self._orders)

    def get_by_id(self, order_id: int) -> Order | None:
        for order in self._orders:
            if order.id == order_id:
                return order
        return None

    def add(self, order: Order) -> Order:
        self._orders.append(order)
        return order

    def update(self, order_id: int, update_data: dict) -> Order | None:
        for index, order in enumerate(self._orders):
            if order.id == order_id:
                updated = order.model_copy(update=update_data)
                self._orders[index] = updated
                return updated
        return None

    def delete(self, order_id: int) -> bool:
        for index, order in enumerate(self._orders):
            if order.id == order_id:
                del self._orders[index]
                return True
        return False