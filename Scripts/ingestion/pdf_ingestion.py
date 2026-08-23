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

# Chemin vers ton fichier PDF (Modifie si besoin)
PDF_PATH = Path("Data/uploads/Test.pdf")

# =========================================================
# CONNEXION
# =========================================================
client = QdrantClient(
    url=QDRANT_URL,
    check_compatibility=False  # Ignore les avertissements de version
)

model = SentenceTransformer(MODEL_NAME)

# Vérifier si la collection existe, sinon la créer
print(f"Checking if collection '{COLLECTION_NAME}' exists...")
if not client.collection_exists(COLLECTION_NAME):
    print(f"Creating collection '{COLLECTION_NAME}'...")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    print("Collection created successfully.")
else:
    print("Collection already exists.")

# =========================================================
# INGESTION DU PDF
# =========================================================
def ingest_pdf(pdf_path: Path):
    if not pdf_path.exists():
        print(f"ERROR: File not found at {pdf_path}")
        return

    print(f"Ingesting file: {pdf_path.name}")

    # 1. Extraire les pages
    pages = extract_pages_from_pdf(str(pdf_path))
    
    points = []
    
    for page in pages:
        page_number = page["page"]
        text = page["text"]
        
        # 2. Découper en chunks
        chunks = chunk_text(text)  # Utilise ton chunker
        
        # 3. Encoder et préparer les points
        for chunk_index, chunk in enumerate(chunks):
            vector = model.encode(chunk, normalize_embeddings=True).tolist()
            
            # Créer un ID unique pour ce chunk
            point_id = str(uuid.uuid4())
            
            point = PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "filename": pdf_path.name,
                    "file_name": pdf_path.name,
                    "page": page_number,
                    "chunk_id": f"{pdf_path.stem}_page_{page_number}_chunk_{chunk_index}",
                    "text": chunk,
                    "path": str(pdf_path)
                }
            )
            points.append(point)

    # 4. Insérer dans Qdrant
    if points:
        print(f"Inserting {len(points)} points into Qdrant...")
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print("Ingestion completed successfully!")
    else:
        print("No points to insert.")

if __name__ == "__main__":
    ingest_pdf(PDF_PATH)