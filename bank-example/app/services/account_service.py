from app.models.account import Account
from app.repositories.account_repository import AccountRepository
from app.services.crypto_service import CryptoService


class AccountService:

    def __init__(self):
        self.repository = AccountRepository()
        self.crypto = CryptoService()

    def create_account(
        self,
        customer_id: int,
        account_number: str,
        balance: str,
    ) -> int:

        account = Account(
            id=None,
            customer_id=customer_id,
            account_number_encrypted=self.crypto.encrypt(account_number),
            balance_encrypted=self.crypto.encrypt(str(balance)),
        )

        return self.repository.create(account)

    def get_account(self, account_id: int):
        row = self.repository.find_by_id(account_id)

        if not row:
            return None

        return {
            "id": row["id"],
            "customer_id": row["customer_id"],
            "account_number": self.crypto.decrypt(
                row["account_number_encrypted"]
            ),
            "balance": self.crypto.decrypt(
                row["balance_encrypted"]
            ),
        }
