# Bank Security Lab - FastAPI

Educational Python + FastAPI application demonstrating:

- MD5 hashing (legacy/insecure demonstration only)
- SHA-256 hashing
- AES-256-GCM encryption/decryption
- MVC-style architecture
- Repository pattern
- SQLite database
- Docker
- FastAPI automatic Swagger/OpenAPI documentation

## Architecture

```text
HTTP Request
     |
     v
  Routes
     |
     v
 Controllers
     |
     v
  Services
     |
     v
Repositories
     |
     v
  SQLite
```

## Generate encryption key

```bash
python3 -c 'import os,base64; print(base64.urlsafe_b64encode(os.urandom(32)).decode())'
```

```bash
export BANK_ENCRYPTION_KEY="YOUR_GENERATED_KEY"
```

## Build

```bash
docker build -t bank-security-lab .
```

## Run

```bash
docker run --rm -p 8080:8080 \
  -e BANK_ENCRYPTION_KEY="$BANK_ENCRYPTION_KEY" \
  bank-security-lab
```

Swagger UI:

http://localhost:8080/docs

ReDoc:

http://localhost:8080/redoc

## Hash demo

```bash
curl -X POST http://localhost:8080/crypto/hash-demo \
  -H "Content-Type: application/json" \
  -d '{"data":"hello world"}'
```

## Create customer

```bash
curl -X POST http://localhost:8080/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "ssn": "123-45-6789",
    "password": "MyPassword123"
  }'
```

## Get customer

```bash
curl http://localhost:8080/customers/1
```

## Create account

```bash
curl -X POST http://localhost:8080/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "account_number": "987654321",
    "balance": "15000.75"
  }'
```

## Get account

```bash
curl http://localhost:8080/accounts/1
```

## Validate encrypted data in SQLite

After creating customers and accounts, inspect the database directly from inside the container.

Regular SQLite CLI approach:

```bash
docker exec -it <container_id> bash
sqlite3 bank.db "SELECT id, name_encrypted, ssn_encrypted FROM customers;"
sqlite3 bank.db "SELECT id, customer_id, account_number_encrypted, balance_encrypted FROM accounts;"
```

Direct command form:

```bash
docker exec -it <container_id> sqlite3 bank.db "SELECT id, name_encrypted, ssn_encrypted FROM customers;"
```

```bash
docker exec -it <container_id> sqlite3 bank.db "SELECT id, customer_id, account_number_encrypted, balance_encrypted FROM accounts;"
```

If the SQLite CLI is not installed in your image, use Python from inside the container instead:

The values in these columns should look like encrypted/base64 output, not plain text. To verify the app decrypts them correctly, use the API endpoints above and compare the returned values with the stored encrypted records.

## Security notes

MD5 is included only to demonstrate why it should not be used for new security applications.

SHA-256 is a cryptographic hash, not encryption. It cannot be decrypted.

AES-256-GCM is used for reversible encryption of sensitive fields.

The password example intentionally uses SHA-256 only to illustrate hashing. In production, use Argon2id, bcrypt, or scrypt with an appropriate password-verification workflow.

For production banking systems, encryption keys should be managed through a KMS/HSM or secrets-management system rather than committed to source code or baked into the image.
