FROM python:3.11-slim

WORKDIR /app

# System deps needed by scikit-learn / pandas wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Train the model at build time so the container is ready to serve immediately.
# (Skips retraining if artifacts already exist, e.g. when copied in from CI cache.)
RUN python -m app.ml.train_model

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
