import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ldap3 import Server, Connection, ALL

app = FastAPI(
    title="LDAP Authentication API",
    description="Educational FastAPI + OpenLDAP example",
    version="1.0.0",
)

LDAP_HOST = os.getenv("LDAP_HOST", "openldap")
LDAP_PORT = int(os.getenv("LDAP_PORT", "389"))
LDAP_BASE_DN = os.getenv("LDAP_BASE_DN", "dc=example,dc=com")


class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/login")
def login(request: LoginRequest):
    server = Server(
        LDAP_HOST,
        port=LDAP_PORT,
        get_info=ALL,
    )

    user_dn = (
        f"uid={request.username},"
        f"ou=users,"
        f"{LDAP_BASE_DN}"
    )

    connection = Connection(
        server,
        user=user_dn,
        password=request.password,
        auto_bind=False,
    )

    try:
        if connection.bind():
            return {
                "authenticated": True,
                "username": request.username,
                "dn": user_dn,
            }

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    finally:
        connection.unbind()
