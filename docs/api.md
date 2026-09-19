# API Guide

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/v1/documents -F "file=@private-report.pdf"
curl -X POST http://localhost:8000/v1/query -H "Content-Type: application/json" \
  -d '{"question":"What are the principal operational risks?","top_k":5}'
```

Answers include `answer`, `citations`, and `request_id`.
