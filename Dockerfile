FROM python:3.12-slim

ENV PYTHONDONWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \

ENV PYTHONPATH=/app

COPY requirements.txt /temp/requirements.txt
COPY . /app

WORKDIR /app

EXPOSE 8000

RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
