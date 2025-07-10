FROM python:3.10-slim

WORKDIR /app

COPY backend/ /app

RUN rm -rf __pycache__ *.ipynb .venv .git .ipynb_checkpoints

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
