import json
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


INPUT_FILE = Path("data/processed/embeddings/PMC7033891_embeddings.json")
COLLECTION_NAME = "medical_articles"
QDRANT_URL = "http://localhost:6333"

def main():
    print("Connecting to Qdrant...")
    client = QdrantClient(url=QDRANT_URL)
    print("Connected successfully")

    print()
    print("Loading embeddings...")
    with open(INPUT_FILE,"r",encoding="utf-8") as file:
        data = json.load(file)

    print(f"Embeddings loaded: {len(data)}")
    print()
    print("Creating collection...")

    existing_collections = [
        collection.name
        for collection in client.get_collections().collections
    ]

    if COLLECTION_NAME in existing_collections:
        print(f"Collection '{COLLECTION_NAME}' already exists.")

    else:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print(f"Collection '{COLLECTION_NAME}' created.")

    print()
    print("Preparing points...")

    points = []

    for index, item in enumerate(data):
        point = PointStruct(
            id=index,
            vector=item["embedding"],
            payload={
                "chunk_id": item["chunk_id"],
                "pmcid": item["pmcid"],
                "path": item["path"],
                "text": item["text"]
            }
        )

        points.append(point)

    print(f"Points prepared: {len(points)}")

    print()
    print("Uploading points to Qdrant...")

    client.upsert(collection_name=COLLECTION_NAME, points=points)

    print("Upload completed")

    print()
    print("==============================")
    print("QDRANT STATISTICS")
    print("==============================")

    info = client.get_collection(collection_name=COLLECTION_NAME)

    print(f"Collection: {COLLECTION_NAME}")
    print(f"Vectors: {info.points_count}")
    print("Vector dimension: 384")
    print("Distance: COSINE")

if __name__ == "__main__":
    main()