from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.services.crypto_service import CryptoService


class CustomerService:

    def __init__(self):
        self.repository = CustomerRepository()
        self.crypto = CryptoService()

    def create_customer(
        self,
        name: str,
        ssn: str,
        password: str,
    ) -> int:

        customer = Customer(
            id=None,
            name_encrypted=self.crypto.encrypt(name),
            ssn_encrypted=self.crypto.encrypt(ssn),
            # Demo only. Production should use Argon2id/bcrypt/scrypt.
            password_hash=self.crypto.sha256(password),
        )

        return self.repository.create(customer)

    def get_customer(self, customer_id: int):
        row = self.repository.find_by_id(customer_id)

        if not row:
            return None

        return {
            "id": row["id"],
            "name": self.crypto.decrypt(row["name_encrypted"]),
            "ssn": self.crypto.decrypt(row["ssn_encrypted"]),
        }
