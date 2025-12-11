from models.order_status import OrderStatus
from models.product import Product
from models.client import Client
from datetime import datetime


class Order:
    def __init__(self, order_id: int, client: Client):
        # Validation check :
        # order_id must be a positive integer
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError('Order ID must be positive integer')

        # client must be Client type
        if not isinstance(client, Client):
            raise ValueError('Client must be an instance of Client')

        self._order_id = order_id
        self._client = client
        self._items = []
        self._status = OrderStatus.NEW
        self._created_at = datetime.now()

    def add_item(self, product: Product):
        if not isinstance(product, Product):
            raise ValueError("Product must be an instance of Product")
        self._items.append(product)
        return f"Product '{product._name}' added to order {self._order_id}"

    def remove_item(self, product):
        if product not in self._items:
            raise ValueError("Item not found in order")
        self._items.remove(product)
        return f"Product '{product._name}' removed from order {self._order_id}"

    def calculate_total(self):
        return sum(item.calculate_price() for item in self._items)

    def mark_paid(self):
        if self._status == OrderStatus.CANCELED:
            raise Exception('Cannot pay for canceled order')

        if self._status == OrderStatus.PAID:
            raise Exception('Cannot pay for paid order')

        self._status = OrderStatus.PAID
        return f"Order {self._order_id} has been paid"

    def cancel(self):
        if self._status == OrderStatus.PAID:
            raise Exception('Cannot cancel paid order')

        if self._status == OrderStatus.CANCELED:
            raise Exception('The order is already canceled')

        self._status = OrderStatus.CANCELED
        return f"Order {self._order_id} has been canceled"
