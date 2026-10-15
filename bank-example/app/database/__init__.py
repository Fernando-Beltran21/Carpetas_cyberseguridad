from app.database.connection import get_connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_encrypted TEXT NOT NULL,
            ssn_encrypted TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            account_number_encrypted TEXT NOT NULL,
            balance_encrypted TEXT NOT NULL,
            FOREIGN KEY(customer_id)
                REFERENCES customers(id)
        )
    """)

    connection.commit()
    connection.close()
