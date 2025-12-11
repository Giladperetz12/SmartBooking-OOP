from models.product import Product


class PhysicalProduct(Product):
    def __init__(self, product_id: int, name: str, category: str, base_price: float, stock: int, weight: float,
                 shipping_cost: float):
        super().__init__(product_id, name, category, base_price)

        # Validation checks :
        # stock must be integer ≥ 0
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("Stock must be a non-negative integer")

        # weight must be a positive number (float or int)
        if not isinstance(weight, (int, float)) or weight <= 0:
            raise ValueError("Weight must be a positive number")

        # shipping_cost can be 0 or higher
        if not isinstance(shipping_cost, (float, int)) or shipping_cost < 0:
            raise ValueError("Shipping cost must be zero or positive")

        self._stock = stock
        self._weight = float(weight)
        self._shipping_cost = float(shipping_cost)

    def calculate_price(self):
        return self._base_price + self._shipping_cost
