from manager.business_manager import BusinessManager
from models.client import Client
from models.product import Product
from models.service import Service
from models.physical_product import PhysicalProduct
from utils.database_manager import DatabaseManager


def main():
    bm = BusinessManager()
    client = Client(1,"tets","test@mail.com","0543055713")
    print(bm.add_client(client))



def test():
    db = DatabaseManager()
    conn = db.connect()
    print("Connected : ", conn)
    db.create_clients_table()
    print(f"Client Table Created")
    db.create_products_table()
    print(f"Product Table Created")
    db.create_service_table()
    print(f"Service Table Created")
    db.create_physical_product_table()
    print(f"Physical Product Table Created")
    db.create_orders_table()
    print(f"Orders Table Created")
    db.create_order_items_table()
    print(f"Order Items Table Created")
    db.create_payments_table()
    print(f"Payments Table Created")
    db.close()
    print("Closed : ", conn)


if __name__ == "__main__":
    # main()
    test()
