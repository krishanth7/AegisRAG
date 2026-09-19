import argparse,json
from pathlib import Path
from aegisrag.config import get_settings
from aegisrag.services.ingestion import IngestionService
from aegisrag.services.qa import QAService
from aegisrag.services.retrieval import RetrievalService
from aegisrag.vectorstore import build_vector_store

def main()->None:
    p=argparse.ArgumentParser(prog="aegisrag"); s=p.add_subparsers(dest="command",required=True)
    i=s.add_parser("ingest"); i.add_argument("pdf",type=Path)
    q=s.add_parser("query"); q.add_argument("question"); q.add_argument("--top-k",type=int)
    a=p.parse_args(); settings=get_settings(); store=build_vector_store(settings)
    result=IngestionService(settings,store).ingest(a.pdf) if a.command=="ingest" else QAService(settings,RetrievalService(store,settings.top_k)).answer(a.question,a.top_k).model_dump()
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
