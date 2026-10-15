# Asymmetric Cryptography API

A small educational REST API demonstrating **asymmetric encryption and decryption with RSA** using Python, FastAPI, Docker, and an MVC-style structure.

## What this exercise demonstrates

The API uses:

- RSA 2048-bit keys
- RSA-OAEP
- SHA-256
- A public key for encryption
- A private key for decryption
- Base64 encoding for transporting ciphertext through JSON
- FastAPI
- Docker

The `cryptography` library recommends RSA-OAEP for new RSA encryption applications. The public key encrypts the message and the corresponding private key decrypts it.


## Architecture

```text
Client
  |
  | POST /crypto/encrypt
  | plaintext
  v
Controller / FastAPI
  |
  v
CryptoService
  |
  +--> RSA Public Key
  |
  v
Ciphertext (Base64)
  |
  v
Client
  |
  | POST /crypto/decrypt
  | ciphertext
  v
CryptoService
  |
  +--> RSA Private Key
  |
  v
Plaintext
```

Project structure:

```text
.
├── app/
│   ├── main.py
│   ├── models/
│   │   └── crypto.py
│   └── services/
│       └── crypto_service.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
└── README.md
```

## Run with Docker

Build and start:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

## Test encryption

```bash
curl -X POST http://localhost:8000/crypto/encrypt   -H "Content-Type: application/json"   -d '{"message":"Hello Cybersecurity!"}'
```

Example response:

```json
{
  "ciphertext": "..."
}
```

Copy the returned ciphertext.

## Test decryption

```bash
curl -X POST http://localhost:8000/crypto/decrypt   -H "Content-Type: application/json"   -d '{"message":"PASTE_CIPHERTEXT_HERE"}'
```

Expected response:

```json
{
  "plaintext": "Hello Cybersecurity!"
}
```


## Inspect the keys

List Docker volumes:

```bash
docker volume ls
```

The application stores:

```text
/app/keys/private_key.pem
/app/keys/public_key.pem
```

The private key is intentionally kept inside the container volume and is never returned by the API.

## Important RSA limitation

Do not use this endpoint to encrypt arbitrary large files or long messages.

With RSA-2048 and OAEP using SHA-256, the plaintext has a relatively small maximum size. For larger data, use:

```text
AES-GCM
   |
   | encrypt data
   v
Ciphertext

RSA-OAEP
   |
   | encrypt AES key
   v
Encrypted AES key
```

This is called **hybrid encryption**.

## Security concepts

### Confidentiality

Anyone with the public key can encrypt a message, but only the holder of the private key can decrypt it.

```text
Public Key
    |
    v
Encrypt
    |
    v
Ciphertext
    |
    v
Private Key
    |
    v
Plaintext
```

### OAEP

OAEP is used instead of raw RSA. The Python `cryptography` documentation recommends OAEP for new RSA encryption applications.

### Key size

This example uses RSA-2048, which is a reasonable default for a current educational example. The private key uses PKCS#8 PEM serialization.

## Stop the application

```bash
docker compose down
```

To also remove the generated RSA keys stored in the Docker volume:

```bash
docker compose down -v
```

The next startup will generate a new key pair.
