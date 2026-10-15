from dataclasses import dataclass


@dataclass
class Account:
    id: int | None
    customer_id: int
    account_number_encrypted: str
    balance_encrypted: str
