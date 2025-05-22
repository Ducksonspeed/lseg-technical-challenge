FROM python:3.11-slim AS base

WORKDIR /app

COPY . .

FROM base AS test

RUN pip install --no-cache-dir pytest

CMD ["pytest", "tests/"]

FROM base AS cli

ENTRYPOINT ["python", "log_monitor.py"]