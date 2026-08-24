from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from pathlib import Path

# Import de votre fonction d'ingestion
from Scripts.ingestion.pdf_ingestion import ingest_pdf

router = APIRouter()

UPLOAD_DIR = Path("Data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Sauvegarder le fichier localement
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Ingérer dans Qdrant (Cette fonction est synchrone et bloque jusqu'à la fin)
    try:
        print(f"Uploading and ingesting: {file.filename}")
        ingest_pdf(file_path)
        
        # Retourner une réponse positive immédiatement après l'ingestion
        return {
            "message": "PDF uploaded and ingested successfully",
            "filename": file.filename.lower(),  # Renvoyer le nom en minuscules
            "points": getattr(file_path, 'stat', lambda: 0)()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during ingestion: {str(e)}")