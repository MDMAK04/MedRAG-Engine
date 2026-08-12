import json
from pathlib import Path

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


COLLECTION_NAME = "medical_articles"
QDRANT_URL = "http://localhost:6333"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K = 5


def load_embedding_model():
    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Model loaded")

    return model


def create_question_embedding(model, question):
    print("Creating question embedding...")

    embedding = model.encode(
        question,
        normalize_embeddings=True
    )

    print("Question embedding created")

    return embedding.tolist()


def retrieve_chunks(client, question_embedding):
    print("Searching Qdrant...")

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_embedding,
        limit=TOP_K
    ).points

    return results


def retrieve(question):
    print("Connecting to Qdrant...")

    client = QdrantClient(url=QDRANT_URL)

    print("Connected successfully")

    model = load_embedding_model()

    question_embedding = create_question_embedding(
        model,
        question
    )

    results = retrieve_chunks(
        client,
        question_embedding
    )

    return results


def main():

    question = (
        "What is the association between family history "
        "of stroke and ischemic stroke risk?"
    )

    print()
    print("Question:")
    print(question)

    results = retrieve(question)

    print()
    print("==============================")
    print("RETRIEVED CHUNKS")
    print("==============================")

    for rank, result in enumerate(results, start=1):

        print()
        print(f"Rank: {rank}")
        print(f"Score: {result.score}")

        payload = result.payload

        print(f"Chunk ID: {payload.get('chunk_id')}")
        print(f"PMCID: {payload.get('pmcid')}")
        print(f"Path: {payload.get('path')}")

        print()
        print("Text:")
        print(payload.get("text"))


if __name__ == "__main__":
    main()