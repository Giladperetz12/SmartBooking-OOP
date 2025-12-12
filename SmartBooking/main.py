from manager.business_manager import BusinessManager
from models.client import Client
from models.product import Product
from models.service import Service
from models.physical_product import PhysicalProduct
from utils.database_manager import DatabaseManager


def main():
    db = DatabaseManager()
    conn = db.connect()
    print("Connected : ",conn)

    db.create_clients_table()
    print(f"Client Table Created")

    db.close()
    print("Closed : ",conn)


def test():
    test_manager = BusinessManager()
    # Test 1 : adding a client
    print(test_manager.add_client(Client(1, "Gilad", "gilad@test.com", "0501234567")))
    # Test 2 : adding a product
    print(test_manager.add_product(Service(10, "Haircut", "Service", 50, 30, False)))
    # Test 3 : creating an order :
    order = test_manager.create_order(100, 1)
    print(order)
    # Test 4 : adding item to order :
    print(test_manager.add_item_to_order(100, 10))





if __name__ == "__main__":
    main()
    # test()

