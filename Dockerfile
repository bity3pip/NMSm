FROM python:3.12-slim

ENV PYTHONDONWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \

WORKDIR /app

COPY requirements.txt /temp/requirements.txt
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt

EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
