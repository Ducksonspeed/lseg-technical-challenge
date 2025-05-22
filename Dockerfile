FROM python:3.11-slim AS base

WORKDIR /app

COPY . .

FROM base AS tests

RUN pip install --no-cache-dir -r requirements.txt

CMD ["pytest", "tests/"]

FROM base AS cli

ENTRYPOINT ["python", "log_monitor.py"]