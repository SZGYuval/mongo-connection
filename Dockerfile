FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY application/app.py ./app.py

EXPOSE 80

CMD ["python", "app.py"]