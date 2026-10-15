from app.database.connection import get_connection
from app.models.account import Account


class AccountRepository:

    def create(self, account: Account) -> int:
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO accounts (
                    customer_id,
                    account_number_encrypted,
                    balance_encrypted
                )
                VALUES (?, ?, ?)
                """,
                (
                    account.customer_id,
                    account.account_number_encrypted,
                    account.balance_encrypted,
                ),
            )

            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def find_by_id(self, account_id: int):
        connection = get_connection()

        try:
            return connection.execute(
                """
                SELECT
                    id,
                    customer_id,
                    account_number_encrypted,
                    balance_encrypted
                FROM accounts
                WHERE id = ?
                """,
                (account_id,),
            ).fetchone()
        finally:
            connection.close()
