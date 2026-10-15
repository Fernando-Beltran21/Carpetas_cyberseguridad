from app.database.connection import get_connection
from app.models.customer import Customer


class CustomerRepository:

    def create(self, customer: Customer) -> int:
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO customers (
                    name_encrypted,
                    ssn_encrypted,
                    password_hash
                )
                VALUES (?, ?, ?)
                """,
                (
                    customer.name_encrypted,
                    customer.ssn_encrypted,
                    customer.password_hash,
                ),
            )

            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def find_by_id(self, customer_id: int):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    id,
                    name_encrypted,
                    ssn_encrypted,
                    password_hash
                FROM customers
                WHERE id = ?
                """,
                (customer_id,),
            ).fetchone()
        finally:
            connection.close()
