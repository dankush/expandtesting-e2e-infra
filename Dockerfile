FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV ENVIRONMENT=docker
ENV LOG_LEVEL=INFO

CMD ["pytest", "-v", "-m", "integration", "--log-cli-level=INFO", "tests/integration/test_health_check.py"]