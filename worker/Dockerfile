FROM python:3.11-slim
WORKDIR /app
COPY worker/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY backend /workspace/paper-analytics-platform/backend
COPY worker /app
ENV PYTHONPATH=/workspace/paper-analytics-platform/backend
CMD ["python", "app/worker.py"]
