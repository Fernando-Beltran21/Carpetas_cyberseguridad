from fastapi import APIRouter

from app.controllers.customer_controller import CustomerController
from app.schemas.customer import CustomerCreate, CustomerResponse


customer_routes = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)

controller = CustomerController()


@customer_routes.post(
    "",
    response_model=CustomerResponse,
    status_code=201,
)
def create_customer(data: CustomerCreate):
    return controller.create(data)


@customer_routes.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(customer_id: int):
    return controller.get(customer_id)
