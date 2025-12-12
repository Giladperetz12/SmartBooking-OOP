from models.physical_product import PhysicalProduct
from models.product import Product
from models.service import Service
from repositories.client_repository import ClientRepository
from repositories.product_repository import ProductRepository
from repositories.order_repository import OrderRepository
from repositories.payment_repository import PaymentRepository
from models.client import Client
from models.order_status import OrderStatus
from payments.payment import Payment
from payments.cash_payment import CashPayment
from payments.bank_transfer_payment import BankTransferPayment
from payments.credit_card_payment import CreditCardPayment


class BusinessManager:

    def __init__(self):
        self.client_repo = ClientRepository()
        self.product_repo = ProductRepository()
        self.order_repo = OrderRepository()
        self.payment_repo = PaymentRepository()

    def add_client(self, client):
        return self.client_repo.add_client(client)

    def get_client(self, client_id: int):
        return self.client_repo.get_client(client_id)

    def add_product(self, product):
        return self.product_repo.add_product(product)

    def get_product(self, product_id: int):
        return self.product_repo.get_product(product_id)

    def create_order(self, order_id: int, client_id: int):
        return self.order_repo.create_order(order_id, client_id)

    def add_item_to_order(self, order_id: int, product_id: int):
        order = self.order_repo.add_item_to_order(order_id, product_id)
        product = self.product_repo.get_product(product_id)

        if isinstance(product, PhysicalProduct):
            if product._stock <= 0:
                raise ValueError("Product out of stock")

        res = self.order_repo.add_item_to_order(order_id, product_id)
        if isinstance(product,PhysicalProduct):
            product._stock -= 1
            self.product_repo.add_product(product)
        return res

    def cancel_order(self, order_id: int):
        order = self.order_repo.get_order(order_id)
        if order._status == OrderStatus.CANCELED:
            raise ValueError("Order already canceled")
        if order._status == OrderStatus.PAID:
            raise ValueError("Cannot cancel order that already paid")
        return self.order_repo.update_order_status(order_id, OrderStatus.CANCELED)

    def pay_order(self, order_id: int, payment: Payment):
        order = self.order_repo.get_order(order_id)
        if order._status == OrderStatus.PAID:
            raise ValueError("Cannot pay order that already paid")
        if order._status == OrderStatus.CANCELED:
            raise ValueError("Cannot cancel order that already canceled")
        checkout = order.calculate_total()

        if isinstance(payment, CreditCardPayment):
            payment.process_payment()

        elif isinstance(payment, BankTransferPayment):
            if payment._amount != checkout:
                raise ValueError("Payment amount does not match")
            payment.process_payment()

        elif isinstance(payment, CashPayment):
            if payment._amount < checkout:
                raise ValueError("not enough money !")
            payment.process_payment()
        else:
            raise Exception("Unknown payment type")

        self.payment_repo.add_payment(payment)
        self.order_repo.update_order_status(order_id, OrderStatus.PAID)

        return "Order paid successfully"


