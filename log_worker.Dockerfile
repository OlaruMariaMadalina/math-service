# log_worker.Dockerfile
FROM python:3.11-slim

WORKDIR /log_worker
COPY . /log_worker

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "log_worker.worker"]
