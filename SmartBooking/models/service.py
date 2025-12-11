from models.product import Product


class Service(Product):
    def __init__(self, product_id: int, name: str, category: str, base_price: float, duration: int,
                 requires_specialist: bool):
        super().__init__(product_id, name, category, base_price)

        # duration must be a positive integer
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("Duration must be positive integer")

        # requires_specialist must be boolean
        if not isinstance(requires_specialist, bool):
            raise ValueError("requires_specialist must be a boolean value")

        self._duration = duration
        self._requires_specialist = requires_specialist

    def calculate_price(self):
        multiplier = 1.5
        if self._requires_specialist:
            multiplier += 0.5
        price = self._base_price + (self._duration * multiplier)
        return price
