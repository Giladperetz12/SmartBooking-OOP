import sqlite3

from models.product import Product
from models.service import Service
from models.physical_product import PhysicalProduct
from utils.database_manager import DatabaseManager


class ProductRepository:

    def __init__(self):
        self.db = DatabaseManager()

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise ValueError("product must be of type Product")
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO products (product_id, name, category, base_price, product_type)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    product._product_id, product._name, product._category, product._base_price,
                    "SERVICE" if isinstance(product, Service) else "PHYSICAL"
                )
            )
            if isinstance(product, Service):
                cursor.execute(
                    """
                    INSERT INTO services (product_id, duration, requires_specialist)
                    VALUES (?, ?, ?)
                    """,
                    (
                        product._product_id, product._duration, int(product._requires_specialist)
                    )
                )
            elif isinstance(product, PhysicalProduct):
                cursor.execute(
                    """
                    INSERT INTO physical_products (product_id, stock, weight, shipping_cost)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        product._product_id, product._stock, product._weight, product._shipping_cost
                    )
                )
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Product with this ID already exists")
        return "Product added successfully"

    def get_product(self, product_id: int):
        if not isinstance(product_id, int) or product_id <= 0:
            raise ValueError("product_id must be a positive integer")
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT product_id, name, category, base_price, product_type
            FROM products
            WHERE product_id = ?
            """,
            (product_id,)
        )
        product_row = cursor.fetchone()
        if product_row is None:
            raise ValueError("Product not found")
        product_id, name, category, base_price, product_type = product_row
        if product_type == "SERVICE":
            cursor.execute(
                """
                SELECT duration, requires_specialist
                FROM services
                WHERE product_id = ?
                """,
                (product_id,)
            )
            row = cursor.fetchone()
            return Service(
                product_id=product_id, name=name, category=category, base_price=base_price, duration=row[0],
                requires_specialist=bool(row[1])
            )
        elif product_type == "PHYSICAL":
            cursor.execute(
                """
                SELECT stock, weight, shipping_cost
                FROM physical_products
                WHERE product_id = ?
                """,
                (product_id,)
            )
            row = cursor.fetchone()
            return PhysicalProduct(
                product_id=product_id, name=name, category=category, base_price=base_price, stock=row[0], weight=row[1],
                shipping_cost=row[2]
            )
        else:
            raise ValueError("Unknown product type")

    def get_all_products(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT product_id
            FROM products
            """
        )
        rows = cursor.fetchall()
        products = []
        for (product_id,) in rows:
            products.append(self.get_product_by_id(product_id))
        return products

    def delete_product(self, product_id: int):
        if not isinstance(product_id, int) or product_id <= 0:
            raise ValueError("product_id must be a positive integer")
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE
            FROM products
            WHERE product_id = ?
            """,
            (product_id,)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError("Product not found")
        return f"Product {product_id} deleted successfully"