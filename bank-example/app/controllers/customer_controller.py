from fastapi import HTTPException, status

from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer_service import CustomerService


class CustomerController:

    def __init__(self):
        self.service = CustomerService()

    def create(self, data: CustomerCreate) -> CustomerResponse:
        customer_id = self.service.create_customer(
            name=data.name,
            ssn=data.ssn,
            password=data.password,
        )

        customer = self.service.get_customer(customer_id)

        return CustomerResponse(**customer)

    def get(self, customer_id: int) -> CustomerResponse:
        customer = self.service.get_customer(customer_id)

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

        return CustomerResponse(**customer)
