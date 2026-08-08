FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements_cpu.txt .

RUN pip install --no-cache-dir -r requirements_cpu.txt

COPY . .

EXPOSE 5004

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5004"]
