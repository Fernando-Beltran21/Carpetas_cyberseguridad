docker build -t cia-api .


docker run -it --name cia-api-container -p 8000:8000 cia-api
