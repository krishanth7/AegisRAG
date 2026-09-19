from fastapi.testclient import TestClient
from aegisrag.api.app import app
client=TestClient(app)
def test_health()->None:
    r=client.get("/health"); assert r.status_code==200 and r.json()=={"status":"ok"}
def test_short_query_rejected()->None:
    assert client.post("/v1/query",json={"question":"?"}).status_code==422
def test_non_pdf_rejected()->None:
    r=client.post("/v1/documents",files={"file":("notes.txt",b"text","text/plain")}); assert r.status_code==415
