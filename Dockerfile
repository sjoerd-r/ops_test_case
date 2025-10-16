FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY . .

RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install -e .

ENV PYTHONPATH=/app
ENV PATH="/opt/venv/bin:$PATH"

CMD ["uvicorn", "ops.app.main:app", "--host", "0.0.0.0", "--port", "8000"]