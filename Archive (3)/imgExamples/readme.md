docker build -t ciberseguridad-lab .

docker run -it --name mi-lab ciberseguridad-lab


pip install fastapi "uvicorn[standard]" cryptography
python -m uvicorn cia_api:app --reload