from fastapi import HTTPException, status

from app.schemas.account import AccountCreate, AccountResponse
from app.services.account_service import AccountService


class AccountController:

    def __init__(self):
        self.service = AccountService()

    def create(self, data: AccountCreate) -> AccountResponse:
        account_id = self.service.create_account(
            customer_id=data.customer_id,
            account_number=data.account_number,
            balance=data.balance,
        )

        account = self.service.get_account(account_id)

        return AccountResponse(**account)

    def get(self, account_id: int) -> AccountResponse:
        account = self.service.get_account(account_id)

        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found",
            )

        return AccountResponse(**account)
