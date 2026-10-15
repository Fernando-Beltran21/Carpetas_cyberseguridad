from dataclasses import dataclass


@dataclass
class Customer:
    id: int | None
    name_encrypted: str
    ssn_encrypted: str
    password_hash: str
