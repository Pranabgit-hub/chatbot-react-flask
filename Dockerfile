# Use a minimal Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only the backend folder
COPY backend/ /app

# Remove anything unnecessary (in case it's still copied)
RUN rm -rf __pycache__ .venv .git .ipynb_checkpoints

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Gunicorn will run on
EXPOSE 5000

# Start the Flask app using Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
