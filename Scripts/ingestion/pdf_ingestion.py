import uuid
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer

# Imports locaux
from Scripts.ingestion.pdf_processor import extract_pages_from_pdf
from Scripts.ingestion.chunker import chunk_text

# =========================================================
# CONFIGURATION
# =========================================================
COLLECTION_NAME = "medical_articles"
QDRANT_URL = "http://localhost:6333"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Dossier contenant tous les PDFs
UPLOADS_DIR = Path("Data/uploads")

# =========================================================
# CONNEXION (Singleton)
# =========================================================
_client = None
_model = None

def get_client():
    global _client
    if _client is None:
        _client = QdrantClient(
            url=QDRANT_URL,
            check_compatibility=False
        )
    return _client

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

# =========================================================
# INGESTION DE TOUS LES PDFs
# =========================================================

def ingest_pdf(pdf_path: Path):
    client = get_client()
    model = get_model()

    if not pdf_path.exists():
        print(f"ERROR: File not found at {pdf_path}")
        return

    print(f"Ingesting file: {pdf_path.name}")

    pages = extract_pages_from_pdf(str(pdf_path))
    
    points = []
    
    for page in pages:
        page_number = page["page"]
        text = page["text"]
        
        chunks = chunk_text(text)
        
        for chunk_index, chunk in enumerate(chunks):
            vector = model.encode(chunk, normalize_embeddings=True).tolist()
            
            point_id = str(uuid.uuid4())
            
            # ✅ NORMALISATION : On force le nom en minuscules
            normalized_name = pdf_path.name.lower()
            
            point = PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "filename": normalized_name,
                    "file_name": normalized_name,
                    "page": page_number,
                    "chunk_id": f"{pdf_path.stem}_page_{page_number}_chunk_{chunk_index}",
                    "text": chunk,
                    "path": str(pdf_path)
                }
            )
            points.append(point)

    if points:
        print(f"Inserting {len(points)} points into Qdrant...")
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print("Ingestion completed successfully!")
    else:
        print("No points to insert.")


def ingest_all_pdfs():
    print(f"Searching for PDFs in: {UPLOADS_DIR}")
    pdf_files = UPLOADS_DIR.glob("*.pdf")
    
    for pdf_path in pdf_files:
        ingest_pdf(pdf_path)
        print("-" * 50)


if __name__ == "__main__":
    ingest_all_pdfs()