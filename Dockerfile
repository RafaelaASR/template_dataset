
FROM python:3.11.15-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser

RUN python -m venv $VIRTUAL_ENV

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser backend/ ./

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
