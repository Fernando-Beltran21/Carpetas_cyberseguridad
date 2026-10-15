from fastapi import FastAPI

from app.database import initialize_database
from app.routes.customer_routes import customer_routes
from app.routes.account_routes import account_routes
from app.routes.crypto_routes import crypto_routes


def create_app() -> FastAPI:
    app = FastAPI(
        title="Bank Security Lab",
        description="Educational MVC application demonstrating hashing and encryption",
        version="1.0.0",
    )

    initialize_database()

    app.include_router(customer_routes)
    app.include_router(account_routes)
    app.include_router(crypto_routes)

    return app
