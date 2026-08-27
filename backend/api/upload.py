from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from pathlib import Path

# Import de vos fonctions d'ingestion
from Scripts.ingestion.pdf_ingestion import ingest_pdf

router = APIRouter()

UPLOAD_DIR = Path("Data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ✅ Définir les types de fichiers acceptés
ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".gif", ".bmp"}


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Vérifier l'extension
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF or Image files are allowed")
    
    # Sauvegarder le fichier localement
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Ingérer selon le type de fichier
    try:
        if file_extension == ".pdf":
            print(f"Uploading and ingesting: {file.filename}")
            ingest_pdf(file_path)
            return {"message": "PDF uploaded and ingested successfully", "filename": file.filename.lower()}
        else:
            # ✅ Cas d'une image seule
            print(f"Uploading image: {file.filename}")
            return {"message": "Image uploaded successfully", "filename": file.filename.lower(), "type": "image"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during ingestion: {str(e)}")