# Use official Python base image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy your backend code
COPY backend/ /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8000 (used by gunicorn)
EXPOSE 8000

# Run the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
