import json
from pathlib import Path

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


COLLECTION_NAME = "medical_articles"
QDRANT_URL = "http://localhost:6333"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5

def main():
    print("Connecting to Qdrant...")

    client = QdrantClient(url=QDRANT_URL)
    print("Connected successfully")

    print()
    print("Loading embedding model...")

    model = SentenceTransformer(
        MODEL_NAME
    )

    print("Model loaded")

    question = (
        "What is the association between family history "
        "of stroke and ischemic stroke risk?"
    )

    print()
    print("Question:")
    print(question)

    print()
    print("Creating question embedding...")

    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    print("Question embedding created")

    print()
    print("Searching Qdrant...")

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_embedding,
        limit=TOP_K,
        with_payload=True
    ).points

    print()
    print("==============================")
    print("QDRANT SEARCH RESULTS")
    print("==============================")

    for rank, result in enumerate(
        results,
        start=1
    ):

        print()
        print(f"Rank: {rank}")
        print(f"Score: {result.score:.4f}")

        payload = result.payload

        print(f"Chunk ID: {payload['chunk_id']}")
        print(f"PMCID: {payload['pmcid']}")
        print(f"Path: {payload['path']}")

        print()
        print("Text:")
        print(payload["text"][:700])

        print("-" * 60)


if __name__ == "__main__":
    main()