FROM python:3.9-slim

WORKDIR /app


COPY src/ ./src/
COPY static/ ./static/
COPY pyproject.toml ./

RUN pip install fastapi uvicorn httpx


EXPOSE 8080


CMD ["python", "src/server.py"]