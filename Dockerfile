FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
# --max-instances=1 required in Cloud Run until Firestore replaces in-memory session store
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
