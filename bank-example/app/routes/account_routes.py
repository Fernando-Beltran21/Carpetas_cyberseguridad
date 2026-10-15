from fastapi import APIRouter

from app.controllers.account_controller import AccountController
from app.schemas.account import AccountCreate, AccountResponse


account_routes = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)

controller = AccountController()


@account_routes.post(
    "",
    response_model=AccountResponse,
    status_code=201,
)
def create_account(data: AccountCreate):
    return controller.create(data)


@account_routes.get(
    "/{account_id}",
    response_model=AccountResponse,
)
def get_account(account_id: int):
    return controller.get(account_id)
