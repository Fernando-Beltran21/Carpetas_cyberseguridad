from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1)
    ssn: str = Field(min_length=1)
    password: str = Field(min_length=1)


class CustomerResponse(BaseModel):
    id: int
    name: str
    ssn: str
