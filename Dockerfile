# Use slim Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only backend source code
COPY backend/ /app

# Avoid cache from virtual environments or model files
RUN rm -rf venv *.pt *.pkl __pycache__ .venv

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default Flask port
EXPOSE 5000

# Start the app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
