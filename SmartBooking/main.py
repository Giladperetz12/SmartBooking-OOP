from datetime import datetime
from abc import ABC, abstractmethod
from typing import List
from enum import Enum


def main():
    print("Test")


if __name__ == '__main__':
    main()


class Client:
    def __init__(self, client_id: int, name: str, email: str, phone_number: str):
        # checking validation

        # client id must be a positive integer
        if not isinstance(client_id, int) or client_id <= 0:
            raise ValueError('Client ID must be positive integer')

        # the name must not be an empty string
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError('Name cannot be an empty string')

        # the phone number must be string of digits with normal length
        if (
                not isinstance(phone_number, str) or
                not phone_number.isdigit() or
                len(phone_number) > 12 or
                len(phone_number) < 9
        ):
            raise ValueError("Phone number must contain only digits and be 9–12 characters long")

        # basic email validation - domain , length etc..
        if not isinstance(email, str) or '@' not in email or '.' not in email.split('@')[-1]:
            raise ValueError("Invalid email address")

        self._client_id = client_id
        self._name = name
        self._email = email
        self._phone_number = phone_number
        self._orders = []


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


class OrderStatus(Enum):
    NEW = "NEW"
    PAID = "PAID"
    CANCELED = "CANCELED"


class Order:
    def __init__(self, order_id: int, client: Client):
        # Validation check :
        # order_id must be a positive integer
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError('Order ID must be positive integer')

        # client must be Client type
        if not isinstance(client, Client):
            raise ValueError('Client must be an instance of Client')

        self._order_id = order_id
        self._client = client
        self._items = []
        self._status = OrderStatus.NEW
        self._created_at = datetime.now()

    def add_item(self, product: Product):
        if not isinstance(product, Product):
            raise ValueError("Product must be an instance of Product")
        self._items.append(product)
        return f"Product '{product._name}' added to order {self._order_id}"

    def remove_item(self, product):
        if product not in self._items:
            raise ValueError("Item not found in order")
        self._items.remove(product)
        return f"Product '{product._name}' removed from order {self._order_id}"

    def calculate_total(self):
        return sum(item.calculate_price() for item in self._items)

    def mark_paid(self):
        if self._status == OrderStatus.CANCELED:
            raise Exception('Cannot pay for canceled order')

        if self._status == OrderStatus.PAID:
            raise Exception('Cannot pay for paid order')

        self._status = OrderStatus.PAID
        return f"Order {self._order_id} has been paid"

    def cancel(self):
        if self._status == OrderStatus.PAID:
            raise Exception('Cannot cancel paid order')

        if self._status == OrderStatus.CANCELED:
            raise Exception('The order is already canceled')

        self._status = OrderStatus.CANCELED
        return f"Order {self._order_id} has been canceled"


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
            if exist_order._order_id== order_id:
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
        if isinstance(product,PhysicalProduct):
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



