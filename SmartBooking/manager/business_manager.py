from models.client import Client
from models.product import Product
from models.order import Order
from models.physical_product import PhysicalProduct
from payments.payment import Payment
from payments.cash_payment import CashPayment
from payments.credit_card_payment import CreditCardPayment
from payments.bank_transfer_payment import BankTransferPayment


class BusinessManager:
    def __init__(self):
        self._clients = []
        self._products = []
        self._orders = []
        self._payments = []

    def add_client(self, client: Client):
        if not isinstance(client, Client):
            raise ValueError("Client must be a Client")
        for exist_client in self._clients:
            if exist_client._client_id == client._client_id:
                raise Exception("Client ID already registered")
        self._clients.append(client)
        return 'Client registered'

    def get_client(self, client_id: int):
        if client_id <= 0 or not isinstance(client_id, int):
            raise ValueError("Client ID must be a valid id : Positive Integer")
        for exist_client in self._clients:
            if exist_client._client_id == client_id:
                return exist_client
        raise ValueError("Client not found")

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise ValueError("Product must be a valid Product type")
        for exist_product in self._products:
            if exist_product._product_id == product._product_id:
                raise Exception("Product ID already registered")
        self._products.append(product)
        return 'Product registered'

    def get_product(self, product_id: int):
        if not isinstance(product_id, int) or product_id <= 0:
            raise ValueError("Product ID must be a valid id : Positive Integer")
        for exist_product in self._products:
            if exist_product._product_id == product_id:
                return exist_product
        raise ValueError("Product not found")

    def create_order(self, order_id: int, client_id: int):
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("Order ID must be a valid id : Positive Integer")
        if not isinstance(client_id, int) or client_id <= 0:
            raise ValueError("Client ID must be a valid id : Positive Integer")
        for exist_order in self._orders:
            if exist_order._order_id == order_id:
                raise ValueError("Order ID already registered")
        client = self.get_client(client_id)
        new_order = Order(order_id, client)
        self._orders.append(new_order)
        return new_order

    def add_item_to_order(self, order_id: int, product_id: int):
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("Order ID must be a valid id : Positive Integer")
        if not isinstance(product_id, int) or product_id <= 0:
            raise ValueError("Product ID must be a valid id : Positive Integer")
        order = self.get_order(order_id)
        product = self.get_product(product_id)
        if isinstance(product, PhysicalProduct):
            if product._stock <= 0:
                raise Exception("Product out of stock")
            product._stock -= 1
        return order.add_item(product)

    def pay_order(self, order_id: int, payment: Payment):
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("Order ID must be a positive integer")
        if not isinstance(payment, Payment):
            raise ValueError("Payment must be a Payment object")
        order = self.get_order(order_id)
        checkout = order.calculate_total()
        if isinstance(payment, CreditCardPayment):
            if payment._amount != checkout:
                raise Exception(f"Credit card payment must be exactly {checkout}")
            payment.process_payment()
            message = order.mark_paid()
            self._payments.append(payment)
            return message
        elif isinstance(payment, BankTransferPayment):
            if payment._amount != checkout:
                raise Exception(f"Bank transfer amount must be exactly {checkout}")
            payment.process_payment()
            message = order.mark_paid()
            self._payments.append(payment)
            return message
        elif isinstance(payment, CashPayment):
            if payment._received_amount < checkout:
                raise Exception("Insufficient cash provided")
            payment.process_payment()
            message = order.mark_paid()
            self._payments.append(payment)
            return f"{message}. Change returned: {payment._change}"
        else:
            raise ValueError("Payment type not recognized")

    def cancel_order(self, order_id: int):
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("Order ID must be a valid id : Positive Integer")
        order = self.get_order(order_id)
        order.cancel()

    def get_order(self, order_id: int):
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("Order ID must be a valid id : Positive Integer")
        for exist_order in self._orders:
            if exist_order._order_id == order_id:
                return exist_order
        raise ValueError("Order not found")
