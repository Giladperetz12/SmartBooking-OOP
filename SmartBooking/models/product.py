from abc import ABC , abstractmethod

class Product(ABC):
    @abstractmethod
    def calculate_price(self):
        pass

    def __init__(self, product_id: int, name: str, category: str, base_price: float):
        # checking validation
        # product_id must be positive int
        if not isinstance(product_id, int) or product_id <= 0:
            raise ValueError('Product ID must be positive integer')

        # product name must be valid string name
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError('Product name cannot be an empty string')

        # category must be valid string
        if not isinstance(category, str) or category.strip() == "":
            raise ValueError('Category cannot be an empty string')

        # product base-price must be a positive float
        if not isinstance(base_price, (float, int)) or base_price <= 0.0:
            raise ValueError('Base price must be positive float')

        self._product_id = product_id
        self._name = name
        self._category = category
        self._base_price = float(base_price)