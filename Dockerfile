FROM python:3.10-slim

WORKDIR /app

# Copy only what’s needed
COPY backend/ /app

# System packages (only if needed — comment out if not)
RUN apt-get update && apt-get install -y gcc g++ wget && rm -rf /var/lib/apt/lists/*

# Clean up unnecessary files before install
RUN rm -rf __pycache__ *.ipynb .venv .git .ipynb_checkpoints

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
