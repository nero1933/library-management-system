FROM python:3.11-alpine
LABEL authors="nero"

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN apk add --no-cache gcc musl-dev libffi-dev

EXPOSE 8000

CMD ["python", "main.py"]

ENV PYTHONPATH=/app
