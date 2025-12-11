from datetime import datetime
from models.order import Order
from payments.payment import Payment


class CashPayment(Payment):
    def __init__(self, payment_id: int, order: Order, amount: float, received_amount: float, date: datetime = None):
        super().__init__(payment_id, order, amount, date)

        if not isinstance(received_amount, (float, int)):
            raise ValueError('Received amount must be a valid number')
        if received_amount < amount:
            raise Exception('Not enough cash received')

        self._received_amount = float(received_amount)
        self._change = self._received_amount - self._amount

    def process_payment(self):
        return f"Cash payment of {self._amount} for order {self._order._order_id} accepted. Change given: {self._change}."
