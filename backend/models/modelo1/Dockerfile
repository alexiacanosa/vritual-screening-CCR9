FROM continuumio/miniconda3

WORKDIR /app

# Copy environment first
COPY environment.yml .

# Install conda env
RUN conda env create -f environment.yml

# Use the environment
SHELL ["conda", "run", "-n", "modelo1", "/bin/bash", "-c"]

# Copy the code
COPY . .

# EXPOSE internal port
EXPOSE 5001

# Run FastAPI app (adjust if Flask)
CMD ["conda", "run", "--no-capture-output", "-n", "modelo1", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]
