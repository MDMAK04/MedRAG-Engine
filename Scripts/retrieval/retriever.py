from pathlib import Path
from typing import Optional

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchAny,
)


# =========================================================
# CONFIGURATION
# =========================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

QDRANT_URL = "http://localhost:6333"

COLLECTION_NAME = "medical_articles"

TOP_K = 5


# =========================================================
# QDRANT
# =========================================================

print("Initializing Qdrant...")

client = QdrantClient(
    url=QDRANT_URL
)

print("Qdrant connected")


# =========================================================
# EMBEDDING MODEL
# =========================================================

print("Loading embedding model...")

model = SentenceTransformer(
    MODEL_NAME
)

print("Embedding model loaded")


# =========================================================
# RETRIEVE
# =========================================================

def retrieve(
    question: str,
    pdf_names: Optional[list[str]] = None,
):
    """
    Retrieve the most relevant chunks from Qdrant.

    Parameters
    ----------
    question:
        User question.

    pdf_names:
        Optional list of PDF filenames.

        Example:
        ["Test.pdf"]

        or:

        ["Test.pdf", "Test2.pdf"]
    """

    print("\n" + "=" * 60)
    print("RETRIEVAL")
    print("=" * 60)

    print("Question:", question)
    print("PDF filter:", pdf_names)

    # =====================================================
    # CREATE QUESTION EMBEDDING
    # =====================================================

    print("Creating question embedding...")

    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    print("Question embedding created")

    # =====================================================
    # BUILD QDRANT FILTER
    # =====================================================

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

        print(
            "Qdrant filter created for:",
            pdf_names
        )

    # =====================================================
    # SEARCH QDRANT
    # =====================================================

    print("Searching Qdrant...")

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_embedding,
        query_filter=query_filter,
        limit=TOP_K,
        with_payload=True,
    ).points

    print(
        f"Retrieved {len(results)} chunks"
    )

    # =====================================================
    # FORMAT RESULTS
    # =====================================================

    formatted_results = []

    for result in results:

        payload = result.payload or {}

        formatted_results.append(
            {
                "text": payload.get(
                    "text",
                    ""
                ),

                "score": result.score,

                # Qdrant uses "filename"
                "filename": payload.get(
                    "filename"
                ),

                # Keep file_name too in case
                # another part of the application
                # expects this key.
                "file_name": payload.get(
                    "filename"
                ),

                "page": payload.get(
                    "page"
                ),

                "chunk_id": payload.get(
                    "chunk_id"
                ),

                "path": payload.get(
                    "path"
                ),
            }
        )

    # =====================================================
    # DEBUG
    # =====================================================

    for index, item in enumerate(
        formatted_results,
        start=1
    ):

        print(
            f"\nResult {index}"
        )

        print(
            "File:",
            item["filename"]
        )

        print(
            "Page:",
            item["page"]
        )

        print(
            "Score:",
            item["score"]
        )

        print(
            "Chunk ID:",
            item["chunk_id"]
        )

    return formatted_results