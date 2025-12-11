from datetime import datetime
from models.order import Order
from payments.payment import Payment


class CreditCardPayment(Payment):
    def __init__(self, payment_id: int, order: Order, amount: float, card_number: str, card_holder: str, cvv: str,
                 expiration_date: str,
                 date: datetime = None):

        super().__init__(payment_id, order, amount, date)

        if not isinstance(card_number, str) or not card_number.isdigit():
            raise ValueError('Card number must be a string of digits')
        if len(card_number) != 16:
            raise ValueError('Card number must be 16 digits')

        if not isinstance(card_holder, str) or card_holder.strip() == "":
            raise ValueError('Card holder must be a valid string of a name')
        if not all(ch.isalpha() or ch.isspace() for ch in card_holder):
            raise ValueError('Card holder name must contain only letters and spaces')

        if not isinstance(cvv, (str, int)):
            raise ValueError('The cvv must be a string of digits')
        if isinstance(cvv, int):
            cvv = str(cvv)
        if not cvv.isdigit():
            raise ValueError('The cvv must be a valid numbers without spaces or symbols or letters')
        if len(cvv) != 3:
            raise ValueError('The cvv must be three digits')

        if not isinstance(expiration_date, str):
            raise ValueError("Expiration date must be a string")
        if len(expiration_date) != 5 or expiration_date[2] != "/":
            raise ValueError("Expiration date must be in format MM/YY")
        month, year = expiration_date.split("/")
        if not (month.isdigit() and year.isdigit()):
            raise ValueError("Expiration date must contain digits")
        month = int(month)
        if month < 1 or month > 12:
            raise ValueError("Expiration month must be between 01 and 12")

        self._card_number = card_number
        self._card_holder = card_holder
        self._cvv = cvv
        self._expiration_date = expiration_date

    def process_payment(self):
        month, year = self._expiration_date.split("/")
        current_year = int(datetime.now().year) % 100
        current_month = int(datetime.now().month)
        if int(year) < current_year:
            raise Exception("Card expired")
        if int(year) == current_year:
            if int(month) < current_month:
                raise Exception("Card expired")
        return f"Credit card payment of {self._amount} for order {self._order._order_id} processed successfully."
