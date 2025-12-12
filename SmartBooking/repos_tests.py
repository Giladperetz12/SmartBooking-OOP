from models.client import Client
from models.service import Service
from models.physical_product import PhysicalProduct
from payments.cash_payment import CashPayment

from repositories.client_repository import ClientRepository
from repositories.product_repository import ProductRepository
from repositories.order_repository import OrderRepository
from repositories.payment_repository import PaymentRepository


def test_repositories():
    print("=== START REPOSITORY TESTS ===")

    client_repo = ClientRepository()
    product_repo = ProductRepository()
    order_repo = OrderRepository()
    payment_repo = PaymentRepository()

    # ---- Client ----
    client = Client(2, "Gilad", "gilad@test.com", "0501234567")
    print(client_repo.add_client(client))

    fetched_client = client_repo.get_client(2)
    print("Fetched client:", fetched_client._name)

    # ---- Products ----
    service = Service(
        product_id=109,
        name="Haircut",
        category="Beauty",
        base_price=50.0,
        duration=30,
        requires_specialist=True
    )

    physical = PhysicalProduct(
        product_id=108,
        name="Shampoo",
        category="Beauty",
        base_price=25.0,
        stock=10,
        weight=0.5,
        shipping_cost=5.0
    )

    print(product_repo.add_product(service))
    print(product_repo.add_product(physical))

    # ---- Order ----
    order = order_repo.create_order(order_id=5011, client_id=2)
    print("Order created:", order._order_id)

    print(order_repo.add_item_to_order(5011, 109))
    print(order_repo.add_item_to_order(5011, 108))

    fetched_order = order_repo.get_order(5011)
    print("Order items count:", len(fetched_order._items))

    # ---- Payment ----
    payment = CashPayment(
        payment_id=9001,
        order=fetched_order,
        amount=fetched_order.calculate_total(),
        received_amount=200.0
    )

    print(payment_repo.add_payment(payment))
    print(payment.process_payment())

    print("=== ALL TESTS PASSED ===")


if __name__ == "__main__":
    test_repositories()
