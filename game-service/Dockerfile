FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# default FastAPI port, might need another later on
EXPOSE 8000

COPY . .

CMD [ "python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]