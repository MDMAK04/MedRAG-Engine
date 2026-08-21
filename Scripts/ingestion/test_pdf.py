from pathlib import Path

from pdf_ingestion import ingest_pdf
from retriever import retrieve


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PDF_PATH = (
    PROJECT_ROOT
    / "Data"
    / "uploads"
    / "Test.pdf"
)


# Indexation
result = ingest_pdf(
    str(PDF_PATH)
)

print()
print("=" * 60)
print("INGESTION RESULT")
print("=" * 60)

print(result)


# Recherche
question = (
    "What is the association between atrial fibrillation "
    "and ischemic stroke?"
)

print()
print("=" * 60)
print("TEST RETRIEVAL")
print("=" * 60)

print(f"Question: {question}")

results = retrieve(question)

print()
print(f"Retrieved chunks: {len(results)}")


for index, result in enumerate(
    results,
    start=1
):

    payload = result.payload or {}

    print()
    print("-" * 60)

    print(f"Result {index}")
    print(f"Score: {result.score}")
    print(
        f"Source type: "
        f"{payload.get('source_type')}"
    )
    print(
        f"Filename: "
        f"{payload.get('filename')}"
    )
    print(
        f"Page: "
        f"{payload.get('page')}"
    )
    print(
        f"Chunk ID: "
        f"{payload.get('chunk_id')}"
    )

    print()
    print(
        payload.get("text", "")[:500]
    )