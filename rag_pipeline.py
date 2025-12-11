import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

# New Chroma persistent client
client = chromadb.PersistentClient(path="./chroma_db")

# Create or load collection
collection = client.get_or_create_collection(name="planning_docs")

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str) -> List[float]:
    vec = embedding_model.encode(text)
    arr = np.asarray(vec)
    return [float(x) for x in arr.tolist()]


def add_document(doc_id: str, text: str) -> None:
    embedding = embed_text(text)

    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding]
    )


def retrieve_docs(query: str, k: int = 3) -> List[str]:
    embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=k
    )

    docs = results.get("documents") or []
    flat_docs = [doc for group in docs for doc in group]
    return flat_docs


# Add sample knowledge documents
sample_docs = {
    "doc1": "Event planning requires considering weather, venue capacity, transport, risks, and budget.",
    "doc2": "Travel planning involves traffic patterns, climate, flight delays, emergency backups, and local regulations.",
    "doc3": "Project planning includes timelines, dependencies, resources, workloads, and risk mitigation strategies."
}

# Correct way to fetch existing IDs from Chroma
try:
    peek = collection.peek()  # returns up to first 100 items
    existing_ids = peek.get("ids", [])
except:
    existing_ids = []

# Add sample knowledge documents only once
for doc_id, text in sample_docs.items():
    if doc_id not in existing_ids:
        add_document(doc_id, text)


