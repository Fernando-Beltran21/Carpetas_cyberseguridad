from fastapi import APIRouter

from app.controllers.crypto_controller import CryptoController
from app.schemas.crypto import HashDemoRequest, HashDemoResponse


crypto_routes = APIRouter(
    prefix="/crypto",
    tags=["Cryptography"],
)

controller = CryptoController()


@crypto_routes.post(
    "/hash-demo",
    response_model=HashDemoResponse,
)
def hash_demo(data: HashDemoRequest):
    return controller.hash_demo(data)
