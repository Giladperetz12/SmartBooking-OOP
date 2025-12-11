from datetime import datetime
from models.order import Order
from payments.payment import Payment


class BankTransferPayment(Payment):
    def __init__(self, payment_id: int, order: Order, amount: float, bank_name: str, account_number: str,
                 transfer_id: str,
                 date: datetime = None
                 ):
        super().__init__(payment_id, order, amount, date)

        if not isinstance(bank_name, str) or bank_name.strip() == "":
            raise ValueError("Bank name must be a non-empty string")

        # Optional: ensure bank name is only letters + spaces
        if not all(ch.isalpha() or ch.isspace() for ch in bank_name):
            raise ValueError("Bank name must contain only letters and spaces")

        # --- Validation: account_number ---
        if isinstance(account_number, int):
            account_number = str(account_number)

        if not isinstance(account_number, str) or not account_number.isdigit():
            raise ValueError("Account number must contain digits only")

        if len(account_number) < 6 or len(account_number) > 20:
            raise ValueError("Account number must be between 6 and 20 digits")

        # --- Validation: transfer_id ---
        if not isinstance(transfer_id, str) or transfer_id.strip() == "":
            raise ValueError("Transfer ID must be a non-empty string")

        if len(transfer_id) < 5:
            raise ValueError("Transfer ID must be at least 5 characters long")

        # Assign fields
        self._bank_name = bank_name
        self._account_number = account_number
        self._transfer_id = transfer_id

    def process_payment(self):
        return (
            f"Bank transfer of {self._amount} for order {self._order._order_id} "
            f"completed successfully. Transfer ID: {self._transfer_id}."
        )
