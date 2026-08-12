import json
from pathlib import Path
from sentence_transformers import SentenceTransformer


INPUT_FILE = Path("data/processed/chunks/PMC7033891_chunks.json")
OUTPUT_FILE = Path("data/processed/embeddings/PMC7033891_embeddings.json")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def main():
    print("Loading chunks...")
    with open(INPUT_FILE,"r",encoding="utf-8") as file:
        chunks = json.load(file)

    print(f"Chunks loaded: {len(chunks)}")
    print()
    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)
    print("Embedding model loaded")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print()
    print("Creating embeddings...")

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    print("Embeddings created")
    output_data = []
    for chunk, embedding in zip(chunks, embeddings):
        output_data.append({
            "chunk_id": chunk["chunk_id"],
            "pmcid": chunk["pmcid"],
            "path": chunk["path"],
            "text": chunk["text"],
            "embedding": embedding.tolist()
        })

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output_data,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("==============================")
    print("EMBEDDING STATISTICS")
    print("==============================")

    print(f"Total chunks: {len(output_data)}")

    print(
        f"Embedding dimension: {len(output_data[0]['embedding'])}"
    )

    print(f"Model: {MODEL_NAME}")

    print()
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()