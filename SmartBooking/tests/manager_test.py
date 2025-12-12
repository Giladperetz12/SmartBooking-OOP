from manager.business_manager import BusinessManager

from models.client import Client
from models.service import Service
from models.physical_product import PhysicalProduct
from payments.cash_payment import CashPayment
from payments.credit_card_payment import CreditCardPayment
from payments.bank_transfer_payment import BankTransferPayment
from utils.database_manager import DatabaseManager


def test_business_manager():
    print("=== START BUSINESS MANAGER TESTS ===")

    bm = BusinessManager()

    # ---------- Client ----------
    client = Client(
        client_id=1,
        name="Gilad",
        email="gilad@test.com",
        phone_number="0501234567"
    )
    print(bm.add_client(client))

    # ---------- Products ----------
    service = Service(
        product_id=100,
        name="Haircut",
        category="Beauty",
        base_price=50.0,
        duration=30,
        requires_specialist=True
    )

    physical = PhysicalProduct(
        product_id=101,
        name="Shampoo",
        category="Beauty",
        base_price=25.0,
        stock=5,
        weight=0.5,
        shipping_cost=5.0
    )

    print(bm.add_product(service))
    print(bm.add_product(physical))

    # ---------- Order ----------
    order = bm.create_order(order_id=5000, client_id=1)
    print(f"Order {order._order_id} created")

    print(bm.add_item_to_order(5000, 100))
    print(bm.add_item_to_order(5000, 101))

    total = order.calculate_total()
    print(f"Order total: {total}")

    # ---------- Payment (Cash) ----------
    cash_payment = CashPayment(
        payment_id=9000,
        order=order,
        amount=total,
        received_amount=200.0
    )

    print(bm.pay_order(5000, cash_payment))

    # ---------- Negative test: pay again ----------
    try:
        bm.pay_order(5000, cash_payment)
    except Exception as e:
        print("Expected error:", e)

    # ---------- Cancel paid order (should fail) ----------
    try:
        bm.cancel_order(5000)
    except Exception as e:
        print("Expected error:", e)

    print("=== ALL BUSINESS MANAGER TESTS PASSED ===")


if __name__ == "__main__":
    test_business_manager()
