import sqlite3
from payments.payment import Payment
from payments.cash_payment import CashPayment
from payments.credit_card_payment import CreditCardPayment
from payments.bank_transfer_payment import BankTransferPayment
from utils.database_manager import DatabaseManager


class PaymentRepository:

    def __init__(self):
        self.db = DatabaseManager()

    def add_payment(self, payment: Payment):
        if not isinstance(payment, Payment):
            raise ValueError("payment must be a Payment object")
        conn = self.db.connect()
        cursor = conn.cursor()
        payment_type = self._get_payment_type(payment)
        try:
            cursor.execute(
                """
                INSERT INTO payments (payment_id, order_id, amount, payment_type, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    payment._payment_id, payment._order._order_id, payment._amount, payment_type,
                    payment._date.isoformat()
                )
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Payment with this ID already exists")
        return "Payment added successfully"

    def get_payments_by_order_id(self, order_id: int):
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("Order ID must be a valid id : Positive Integer")
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT payment_id, amount, payment_type, created_at
            FROM payments
            WHERE order_id = ?
            """,
            (order_id,)
        )
        rows = cursor.fetchall()
        payments = []
        for row in rows:
            payment_id, amount, payment_type, created_at = row
            payments.append({
                "payment_id": payment_id,
                "amount": amount,
                "payment_type": payment_type,
                "created_at": created_at
            })
        return payments

    def delete_payment(self, payment_id: int):
        if not isinstance(payment_id, int) or payment_id <= 0:
            raise ValueError("Payment ID must be a valid id : Positive Integer")
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE
            FROM payments
            WHERE payment_id = ?
            """,
            (payment_id,)
        )
        conn.commit()

        if cursor.rowcount == 0:
            raise ValueError("Payment not found")
        return f"Payment {payment_id} deleted successfully"

    def _get_payment_type(self, payment: Payment):
        if isinstance(payment, CashPayment):
            return "CASH"
        if isinstance(payment, CreditCardPayment):
            return "CREDIT_CARD"
        if isinstance(payment, BankTransferPayment):
            return "BANK_TRANSFER"
        raise ValueError("Unknown payment type")
