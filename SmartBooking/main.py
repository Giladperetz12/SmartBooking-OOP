from utils.database_manager import DatabaseManager
from manager.business_manager import BusinessManager


def init() -> BusinessManager:
    db = DatabaseManager()
    db.connect()
    db.init_schema()

    return BusinessManager()


def main():
    bm = init()
    print("SmartBooking system initialized successfully")


if __name__ == "__main__":
    main()
