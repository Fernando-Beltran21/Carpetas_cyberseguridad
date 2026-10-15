from app.schemas.crypto import HashDemoRequest, HashDemoResponse
from app.services.crypto_service import CryptoService


class CryptoController:

    def __init__(self):
        self.crypto = CryptoService()

    def hash_demo(self, data: HashDemoRequest) -> HashDemoResponse:
        return HashDemoResponse(
            input=data.data,
            md5=self.crypto.md5(data.data),
            sha256=self.crypto.sha256(data.data),
        )
