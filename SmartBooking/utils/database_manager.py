import sqlite3


class DatabaseManager():
    def __init__(self, db_name: str = "SmartBooking.db"):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        """Creates a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            return self.conn
        except Exception as e:
            raise Exception(f"failed to connect to the database : {e}")

    def close(self):
        """Close the connection to the SQLite database."""
        if self.conn:
            self.conn.close()

    def create_clients_table(self):
        """Creates the clients table if it does not exist."""
        query = """
                CREATE TABLE IF NOT EXISTS clients \
                ( \
                    client_id \
                    INTEGER \
                    PRIMARY \
                    KEY, \
                    name \
                    TEXT \
                    NOT \
                    NULL, \
                    email \
                    TEXT \
                    NOT \
                    NULL, \
                    phone_number \
                    TEXT \
                    NOT \
                    NULL
                ); \
                """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Failed to create clients table: {e}")
