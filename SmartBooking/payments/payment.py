from abc import ABC, abstractmethod
from datetime import datetime
from models.order import Order


class Payment(ABC):
    @abstractmethod
    def process_payment(self):
        pass

    def __init__(self, payment_id: int, order: Order, amount: float, date: datetime = None):

        if not isinstance(payment_id, int) or payment_id <= 0:
            raise ValueError('Payment ID must be positive integer')

        if not isinstance(order, Order):
            raise ValueError('Order must be an instance of Order')

        if not isinstance(amount, (float, int)):
            raise ValueError('Amount must be a positive number')
        if amount <= 0:
            raise ValueError('Amount must be a positive sum')

        self._payment_id = payment_id
        self._order = order
        self._amount = float(amount)
        self._date = date if date is not None else datetime.now()
