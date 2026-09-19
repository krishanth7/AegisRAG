FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN addgroup --system aegisrag && adduser --system --ingroup aegisrag aegisrag
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --upgrade pip && pip install .
RUN mkdir -p /app/chroma_db /app/uploads && chown -R aegisrag:aegisrag /app
USER aegisrag
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn","aegisrag.api.app:app","--host","0.0.0.0","--port","8000"]
