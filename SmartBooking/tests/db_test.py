from utils.database_manager import DatabaseManager


def test_db():
    db = DatabaseManager()
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables in DB:", tables)

    conn.close()


if __name__ == "__main__":
    test_db()
