FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app/app
COPY .env .
COPY load_data.py .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]