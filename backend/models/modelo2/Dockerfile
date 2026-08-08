# Base image with PyTorch and CUDA
FROM pytorch/pytorch:2.3.1-cuda11.8-cudnn8-runtime

LABEL authors="Colby T. Ford <colby@tuple.xyz>"

# -------------------------
# Install system dependencies
# -------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        git \
        wget \
        gcc \
        g++ \
        curl \
        bzip2 \
        && rm -rf /var/lib/apt/lists/*



WORKDIR /app
COPY . /app  
RUN pip install --no-cache-dir -r requirements.txt

# Expose API port
EXPOSE 5002

RUN apt-get update && apt-get install -y curl

HEALTHCHECK --interval=10s --timeout=5s --retries=30 \
  CMD curl -f http://localhost:5002/health || exit 1


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5002"]

