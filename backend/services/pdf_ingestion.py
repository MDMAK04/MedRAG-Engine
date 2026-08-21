import uuid
from pathlib import Path

from qdrant_client import QdrantClient

from qdrant_client.models import (
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

from sentence_transformers import SentenceTransformer

from Scripts.ingestion.pdf_processor import (
    extract_pages_from_pdf
)

from Scripts.ingestion.chunker import (
    chunk_text
)


# =========================================================
# CONFIGURATION
# =========================================================

COLLECTION_NAME = "medical_articles"

QDRANT_URL = "http://localhost:6333"

MODEL_NAME = (
    "sentence-transformers/"
    "all-MiniLM-L6-v2"
)


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
# CHECK PDF ALREADY INDEXED
# =========================================================

def pdf_already_indexed(
    filename: str
) -> bool:

    try:

        result = client.scroll(
            collection_name=COLLECTION_NAME,

            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="filename",
                        match=MatchValue(
                            value=filename
                        )
                    )
                ]
            ),

            limit=1,

            with_payload=False,

            with_vectors=False
        )

        points = result[0]

        if points:
            print(
                f"PDF already exists in Qdrant: {filename}"
            )

            return True

        return False

    except Exception as e:

        print(
            "Could not check whether PDF "
            f"is already indexed: {e}"
        )

        return False


# =========================================================
# INGEST PDF
# =========================================================

def ingest_pdf(
    pdf_path: str
):

    pdf_path = Path(
        pdf_path
    )

    filename = pdf_path.name

    print()
    print("=" * 60)
    print("PDF INGESTION")
    print("=" * 60)

    print(
        f"File: {filename}"
    )

    print(
        f"Path: {pdf_path}"
    )

    # -----------------------------------------------------
    # Check file
    # -----------------------------------------------------

    if not pdf_path.exists():

        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":

        raise ValueError(
            "Only PDF files are supported."
        )

    # -----------------------------------------------------
    # Check Qdrant collection
    # -----------------------------------------------------

    try:

        collection = client.get_collection(
            COLLECTION_NAME
        )

        print(
            f"Qdrant collection: "
            f"{COLLECTION_NAME}"
        )

        print(
            f"Existing points: "
            f"{collection.points_count}"
        )

    except Exception as e:

        raise RuntimeError(
            "Qdrant collection "
            f"'{COLLECTION_NAME}' "
            f"is not available: {e}"
        )

    # -----------------------------------------------------
    # Prevent duplicate indexing
    # -----------------------------------------------------

    if pdf_already_indexed(
        filename
    ):

        return {
            "filename": filename,
            "chunks": 0,
            "already_indexed": True
        }

    # =====================================================
    # EXTRACT PDF
    # =====================================================

    print()
    print("Extracting PDF pages...")

    pages = extract_pages_from_pdf(
        str(pdf_path)
    )

    if not pages:

        print(
            "No pages extracted."
        )

        return {
            "filename": filename,
            "chunks": 0,
            "already_indexed": False
        }

    print(
        f"Pages extracted: {len(pages)}"
    )

    # =====================================================
    # CREATE QDRANT POINTS
    # =====================================================

    points = []

    total_chunks = 0

    for page_data in pages:

        page_number = page_data.get(
            "page"
        )

        text = page_data.get(
            "text",
            ""
        )

        if not text.strip():

            print(
                f"Page {page_number}: "
                "no text"
            )

            continue

        # -------------------------------------------------
        # Chunk page
        # -------------------------------------------------

        chunks = chunk_text(
            text,
            chunk_size=800,
            chunk_overlap=120
        )

        print(
            f"Page {page_number}: "
            f"{len(chunks)} chunks"
        )

        # -------------------------------------------------
        # Create embeddings
        # -------------------------------------------------

        for chunk_index, chunk in enumerate(
            chunks,
            start=1
        ):

            if not chunk.strip():
                continue

            # ---------------------------------------------
            # Embedding
            # ---------------------------------------------

            embedding = model.encode(
                chunk,
                normalize_embeddings=True
            ).tolist()

            # ---------------------------------------------
            # Chunk ID
            # ---------------------------------------------

            chunk_id = (
                f"{pdf_path.stem}"
                f"_page_{page_number}"
                f"_chunk_{chunk_index}"
            )

            # ---------------------------------------------
            # Payload
            # ---------------------------------------------

            payload = {

                "source_type":
                    "uploaded_pdf",

                "filename":
                    filename,

                "document_id":
                    pdf_path.stem,

                "page":
                    page_number,

                "chunk_id":
                    chunk_id,

                "path":
                    f"PDF page {page_number}",

                "text":
                    chunk
            }

            # ---------------------------------------------
            # Qdrant point
            # ---------------------------------------------

            point = PointStruct(

                id=str(
                    uuid.uuid4()
                ),

                vector=embedding,

                payload=payload
            )

            points.append(
                point
            )

            total_chunks += 1

    # =====================================================
    # NO CHUNKS
    # =====================================================

    if not points:

        print()
        print(
            "No text chunks were generated."
        )

        return {
            "filename": filename,
            "chunks": 0,
            "already_indexed": False
        }

    # =====================================================
    # INSERT INTO QDRANT
    # =====================================================

    print()
    print(
        f"Total chunks: {total_chunks}"
    )

    print(
        "Uploading chunks to Qdrant..."
    )

    try:

        client.upsert(

            collection_name=COLLECTION_NAME,

            points=points,

            wait=True
        )

    except Exception as e:

        print()
        print(
            "QDRANT INSERT ERROR"
        )

        print(
            type(e).__name__
        )

        print(
            str(e)
        )

        raise RuntimeError(
            f"Could not insert PDF chunks "
            f"into Qdrant: {e}"
        )

    # =====================================================
    # VERIFY INSERTION
    # =====================================================

    print(
        "Verifying indexed PDF..."
    )

    verification = client.scroll(

        collection_name=COLLECTION_NAME,

        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="filename",
                    match=MatchValue(
                        value=filename
                    )
                )
            ]
        ),

        limit=1,

        with_payload=True,

        with_vectors=False
    )

    indexed_points = verification[0]

    if not indexed_points:

        raise RuntimeError(
            "Qdrant insertion completed but "
            f"no points were found for '{filename}'."
        )

    print()
    print("=" * 60)
    print("PDF SUCCESSFULLY INDEXED")
    print("=" * 60)

    print(
        f"Filename: {filename}"
    )

    print(
        f"Chunks: {total_chunks}"
    )

    print(
        "Qdrant metadata verified."
    )

    return {
        "filename": filename,
        "chunks": total_chunks,
        "already_indexed": False
    }