from pathlib import Path
from typing import Optional, List

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import Filter, FieldCondition, MatchAny


# =========================================================
# CONFIGURATION
# =========================================================

COLLECTION_NAME = "medical_articles"
QDRANT_URL = "http://localhost:6333"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5

# Création des instances globales (une seule fois)
_client = None
_model = None


def get_client():
    global _client
    if _client is None:
        print("Initializing Qdrant...")
        _client = QdrantClient(
            url=QDRANT_URL,
            check_compatibility=False
        )
        print("Qdrant connected")
    return _client


def get_model():
    global _model
    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(MODEL_NAME)
        print("Embedding model loaded")
    return _model


# =========================================================
# RETRIEVE (Standard)
# =========================================================

def retrieve(
    question: str,
    pdf_names: Optional[list[str]] = None,
):
    client = get_client()
    model = get_model()

    print("\n" + "=" * 60)
    print("RETRIEVAL")
    print("=" * 60)

    print("Question:", question)
    print("PDF filter:", pdf_names)

    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    query_filter = None

    if pdf_names:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="filename",
                    match=MatchAny(
                        any=pdf_names
                    ),
                )
            ]
        )

    print("Searching Qdrant...")

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_embedding,
        query_filter=query_filter,
        limit=TOP_K,
        with_payload=True,
    ).points

    formatted_results = []

    for result in results:
        payload = result.payload or {}
        chunk_id = payload.get("chunk_id", "")

        if chunk_id in [r.get("chunk_id") for r in formatted_results]:
            continue

        formatted_results.append({
            "text": payload.get("text", ""),
            "score": result.score,
            "filename": payload.get("filename"),
            "file_name": payload.get("filename"),
            "page": payload.get("page"),
            "chunk_id": chunk_id,
            "path": payload.get("path"),
        })

    print(f"Retrieved {len(formatted_results)} chunks")

    return formatted_results


# =========================================================
# RETRIEVE BALANCED (Multi-PDF)
# =========================================================

def retrieve_balanced(
    question: str,
    pdf_names: Optional[list[str]] = None,
):
    client = get_client()
    model = get_model()

    print("\n" + "=" * 60)
    print("BALANCED RETRIEVAL (Multi-PDF)")
    print("=" * 60)

    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    formatted_results = []

    if pdf_names and len(pdf_names) > 1:
        # Récupérer des chunks pour chaque PDF individuellement
        for pdf_name in pdf_names:
            print(f"Searching for chunks in: {pdf_name}")
            
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="filename",
                        match=MatchAny(
                            any=[pdf_name]
                        ),
                    )
                ]
            )

            results = client.query_points(
                collection_name=COLLECTION_NAME,
                query=question_embedding,
                query_filter=query_filter,
                limit=3,
                with_payload=True,
            ).points

            for result in results:
                payload = result.payload or {}
                chunk_id = payload.get("chunk_id", "")

                if chunk_id in [r.get("chunk_id") for r in formatted_results]:
                    continue

                formatted_results.append({
                    "text": payload.get("text", ""),
                    "score": result.score,
                    "filename": payload.get("filename"),
                    "file_name": payload.get("filename"),
                    "page": payload.get("page"),
                    "chunk_id": chunk_id,
                    "path": payload.get("path"),
                })
    else:
        formatted_results = retrieve(question=question, pdf_names=pdf_names)

    print(f"Retrieved {len(formatted_results)} chunks from multiple files")
    
    return formatted_results