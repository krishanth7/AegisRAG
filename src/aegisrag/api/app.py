from pathlib import Path
from shutil import copyfileobj
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from aegisrag.api.dependencies import ingestion_service, qa_service
from aegisrag.config import get_settings
from aegisrag.models import AnswerResponse, QueryRequest
from aegisrag.services.ingestion import IngestionService
from aegisrag.services.qa import QAService
from aegisrag.storage import UploadValidationError, allocate_upload_path

app=FastAPI(title="AegisRAG",version="0.1.0",description="Citation-grounded intelligence for private PDF reports.")
@app.get("/health")
def health()->dict[str,str]: return {"status":"ok"}
@app.post("/v1/documents",status_code=status.HTTP_201_CREATED)
def ingest_document(file:UploadFile=File(...),service:IngestionService=Depends(ingestion_service))->dict[str,object]:
    s=get_settings()
    try:
        destination=allocate_upload_path(s.upload_path,file.filename or "report.pdf")
        with destination.open("wb") as output: copyfileobj(file.file,output)
        if destination.stat().st_size>s.max_upload_mb*1024*1024:
            destination.unlink(missing_ok=True); raise HTTPException(413,"Upload exceeds configured limit.")
        return service.ingest(Path(destination))
    except UploadValidationError as exc: raise HTTPException(415,str(exc)) from exc
    finally: file.file.close()
@app.post("/v1/query",response_model=AnswerResponse)
def query(request:QueryRequest,service:QAService=Depends(qa_service))->AnswerResponse:
    return service.answer(request.question,request.top_k)
