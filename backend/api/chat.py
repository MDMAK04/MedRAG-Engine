from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from typing import Optional
import json

from backend.services.agent_orchestrator import orchestrate

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(
    question: str = Form(...),
    selected_pdfs: Optional[str] = Form(None),
    history: Optional[str] = Form(None),
    image_path: Optional[str] = Form(None)  # ✅ Nouveau champ pour les images
):
    print("\n" + "=" * 60)
    print("MEDINTEL CHAT")
    print("=" * 60)
    print("Question:", question)
    
    pdf_list = []
    if selected_pdfs and selected_pdfs.strip():
        try:
            pdf_list = json.loads(selected_pdfs)
        except:
            pdf_list = [selected_pdfs]
    
    # ✅ Gérer les images seules
    image_paths = []
    if image_path and image_path.strip():
        image_paths = [image_path]
    
    try:
        # Appel à l'orchestrateur avec les images
        result = orchestrate(question=question, pdf_names=pdf_list, image_paths=image_paths)
        
        return {
            "answer": result["answer"],
            "sources": result.get("sources", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")