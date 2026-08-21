import uuid
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer

from Scripts.ingestion.pdf_processor import extract_pages_from_pdf
from Scripts.ingestion.chunker import chunk_text


COLLECTION_NAME = "medical_articles"

QDRANT_URL = "http://localhost:6333"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


client = QdrantClient(
    url=QDRANT_URL
)


model = SentenceTransformer(
    MODEL_NAME
)


def ingest_pdf(pdf_path: str):

    pdf_path = Path(pdf_path)

    print()
    print("=" * 60)
    print("PDF INGESTION")
    print("=" * 60)

    print(
        f"File: {pdf_path.name}"
    )

    pages = extract_pages_from_pdf(
        str(pdf_path)
    )

    print(
        f"Pages extracted: {len(pages)}"
    )

    points = []

    total_chunks = 0

    for page_data in pages:

        page_number = page_data["page"]

        text = page_data["text"]

        chunks = chunk_text(
            text,
            chunk_size=800,
            chunk_overlap=120
        )

        print(
            f"Page {page_number}: "
            f"{len(chunks)} chunks"
        )

        for chunk_index, chunk in enumerate(
            chunks,
            start=1
        ):

            if not chunk.strip():
                continue

            embedding = model.encode(
                chunk,
                normalize_embeddings=True
            ).tolist()

            chunk_id = (
                f"{pdf_path.stem}"
                f"_page_{page_number}"
                f"_chunk_{chunk_index}"
            )

            payload = {

                "source_type": "uploaded_pdf",

                "filename": pdf_path.name,

                "document_id": pdf_path.stem,

                "page": page_number,

                "chunk_id": chunk_id,

                "path": (
                    f"PDF page {page_number}"
                ),

                "text": chunk
            }

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload=payload
                )
            )

            total_chunks += 1

    print()

    print(
        f"Total chunks: {total_chunks}"
    )

    if not points:

        print(
            "No chunks found."
        )

        return {
            "filename": pdf_path.name,
            "chunks": 0
        }

    print(
        "Uploading chunks to Qdrant..."
    )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(
        "PDF successfully indexed."
    )

    return {
        "filename": pdf_path.name,
        "chunks": total_chunks
    }