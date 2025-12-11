from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any

# Ensure the current package directory is on sys.path so sibling modules import correctly
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_pipeline import add_document, retrieve_docs

app = FastAPI(title="RAG API")

class DocumentIn(BaseModel):
    id: str
    text: str

@app.get("/")
async def root():
    return {"status": "ok", "service": "RAG API"}

@app.post("/add")
async def add(doc: DocumentIn):
    try:
        add_document(doc.id, doc.text)
        return {"status": "added", "id": doc.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/retrieve")
async def retrieve(query: str, k: int = 3):
    try:
        docs = retrieve_docs(query, k)
        return {"documents": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
