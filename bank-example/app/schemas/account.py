from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    customer_id: int
    account_number: str = Field(min_length=1)
    balance: str = Field(min_length=1)


class AccountResponse(BaseModel):
    id: int
    customer_id: int
    account_number: str
    balance: str
