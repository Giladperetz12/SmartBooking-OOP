import sqlite3
from pathlib import Path


class DatabaseManager:
    def __init__(self, db_name="SmartBooking.db"):
        project_root = Path(__file__).resolve().parents[2]
        self.db_path = project_root / db_name
        self.conn = None

    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA foreign_keys = ON;")
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_clients_table(self):
        """Creates the clients table if it does not exist."""
        query = """
                CREATE TABLE IF NOT EXISTS clients \
                ( \
                    client_id \
                    INTEGER \
                    PRIMARY \
                    KEY, \
                    name \
                    TEXT \
                    NOT \
                    NULL, \
                    email \
                    TEXT \
                    NOT \
                    NULL, \
                    phone_number \
                    TEXT \
                    NOT \
                    NULL
                ); \
                """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Failed to create clients table: {e}")

    def create_products_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS products
                (
                    product_id
                    INTEGER
                    PRIMARY
                    KEY,
                    name
                    TEXT
                    NOT
                    NULL,
                    category
                    TEXT
                    NOT
                    NULL,
                    base_price
                    REAL
                    NOT
                    NULL,
                    product_type
                    TEXT
                    NOT
                    NULL
                ); \
                """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Failed to create products table: {e}")

    def create_service_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS services
                (
                    product_id
                    INTEGER
                    PRIMARY
                    KEY,
                    duration
                    INTEGER
                    NOT
                    NULL,
                    requires_specialist
                    INTEGER
                    NOT
                    NULL,
                    FOREIGN
                    KEY
                (
                    product_id
                ) REFERENCES products
                (
                    product_id
                )
                    ON DELETE CASCADE
                    ); \
                """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Failed to create services table: {e}")

    def create_physical_product_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS physical_products
                (
                    product_id
                    INTEGER
                    PRIMARY
                    KEY,
                    stock
                    INTEGER
                    NOT
                    NULL,
                    weight
                    REAL
                    NOT
                    NULL,
                    shipping_cost
                    REAL
                    NOT
                    NULL,
                    FOREIGN
                    KEY
                (
                    product_id
                ) REFERENCES products
                (
                    product_id
                )
                    ON DELETE CASCADE
                    ); \
                """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Failed to create physical_products table: {e}")

    def create_orders_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS orders
                (
                    order_id
                    INTEGER
                    PRIMARY
                    KEY,
                    client_id
                    INTEGER
                    NOT
                    NULL,
                    status
                    TEXT
                    NOT
                    NULL,
                    created_at
                    TEXT
                    NOT
                    NULL,
                    FOREIGN
                    KEY
                (
                    client_id
                ) REFERENCES clients
                (
                    client_id
                )); \
                """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Failed to create orders table: {e}")

    def create_order_items_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS order_items
                (
                    id
                    INTEGER
                    PRIMARY
                    KEY
                    AUTOINCREMENT,
                    order_id
                    INTEGER
                    NOT
                    NULL,
                    product_id
                    INTEGER
                    NOT
                    NULL,
                    FOREIGN
                    KEY
                (
                    order_id
                ) REFERENCES orders
                (
                    order_id
                )
                    ON DELETE CASCADE,
                    FOREIGN KEY
                (
                    product_id
                ) REFERENCES products
                (
                    product_id
                )); \
                """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Failed to create order_items table: {e}")

    def create_payments_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS payments
                (
                    payment_id
                    INTEGER
                    PRIMARY
                    KEY,
                    order_id
                    INTEGER
                    NOT
                    NULL,
                    amount
                    REAL
                    NOT
                    NULL,
                    payment_type
                    TEXT
                    NOT
                    NULL,
                    created_at
                    TEXT
                    NOT
                    NULL,
                    FOREIGN
                    KEY
                (
                    order_id
                ) REFERENCES orders
                (
                    order_id
                )
                    ON DELETE CASCADE
                    ); \
                """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Failed to create payments table: {e}")
