import sqlite3
from datetime import datetime

from models.order import Order
from models.order_status import OrderStatus
from models.product import Product
from utils.database_manager import DatabaseManager
from repositories.product_repository import ProductRepository
from repositories.client_repository import ClientRepository


class OrderRepository:

    def __init__(self):
        self.db = DatabaseManager()
        self.client_repo = ClientRepository()
        self.product_repo = ProductRepository()

    def create_order(self, order_id: int, client_id: int):
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("Order ID must be a valid id : Positive Integer")

        if not isinstance(client_id, int) or client_id <= 0:
            raise ValueError("Client ID must be a valid id : Positive Integer")
        client = self.client_repo.get_client_by_id(client_id)
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO orders (order_id, client_id, status, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    order_id, client_id, OrderStatus.NEW.value, datetime.now().isoformat()
                )
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Order ID already exists")
        return Order(order_id, client)

    def get_order_by_id(self, order_id: int):
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("Order ID must be a valid id : Positive Integer")
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT order_id, client_id, status, created_at
            FROM orders
            WHERE order_id = ?
            """,
            (order_id,)
        )
        order_row = cursor.fetchone()
        if order_row is None:
            raise ValueError("Order not found")
        order_id, client_id, status, created_at = order_row
        client = self.client_repo.get_client_by_id(client_id)
        order = Order(order_id, client)
        order._status = OrderStatus(status)
        cursor.execute(
            """
            SELECT product_id
            FROM order_items
            WHERE order_id = ?
            """,
            (order_id,)
        )
        product_rows = cursor.fetchall()
        for (product_id,) in product_rows:
            product = self.product_repo.get_product_by_id(product_id)
            order._items.append(product)
        return order

    def add_item_to_order(self, order_id: int, product_id: int):
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("Order ID must be a valid id : Positive Integer")
        if not isinstance(product_id, int) or product_id <= 0:
            raise ValueError("Product ID must be a valid id : Positive Integer")
        self.get_order_by_id(order_id)
        product = self.product_repo.get_product_by_id(product_id)
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO order_items (order_id, product_id)
            VALUES (?, ?)
            """,
            (order_id, product_id)
        )
        conn.commit()
        return f"Product {product_id} added to order {order_id}"

    def delete_order(self, order_id: int):
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("Order ID must be a valid id : Positive Integer")
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE
            FROM orders
            WHERE order_id = ?
            """,
            (order_id,)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError("Order not found")
        return f"Order {order_id} deleted successfully"

    def update_order_status(self, order_id: int, status: OrderStatus):
        if not isinstance(status, OrderStatus):
            raise ValueError("Status must be OrderStatus")
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE orders
            SET status = ?
            WHERE order_id = ?
            """,
            (status.value, order_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError("Order not found")
        return f"Order {order_id} status updated to {status.value}"
