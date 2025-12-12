from models.client import Client
from utils.database_manager import DatabaseManager
import sqlite3


class ClientRepository:
    def __init__(self):
        self.db = DatabaseManager()

    def add_client(self, client: Client):
        if not isinstance(client, Client):
            raise ValueError("Client must be of type Client")
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                           INSERT INTO clients (client_id, name, email, phone_number)
                           VALUES (?, ?, ?, ?)
                           """,
                           (
                               client._client_id, client._name, client._email, client._phone_number
                           )
                           )
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Client with this ID already exists")
        return "Client added successfully"

    def get_client(self, client_id: int):
        if not isinstance(client_id, int):
            raise ValueError("Client id must be a positive integer")
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT client_id, name, email, phone
            FROM clients
            WHERE client_id = ?
            """,
            (client_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise ValueError("Client not found")
        return Client(
            client_id=row[0], name=row[1], email=row[2], phone_number=row[3]
        )

    def get_all_clients(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT client_id, name, email, phone
            FROM clients
            """
        )
        rows = cursor.fetchall()
        clients = []
        for row in rows:
            client = Client(
                client_id=row[0], name=row[1], email=row[2], phone_number=row[3]
            )
            clients.append(client)
        return clients

    def delete_client(self, client_id: int):
        if not isinstance(client_id, int) or client_id <= 0:
            raise ValueError("Client id must be a positive integer")
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE
            FROM clients
            WHERE client_id = ?
            """,
            (client_id,)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise ValueError("Client not found")
        return f"Client {client_id} deleted successfully"

