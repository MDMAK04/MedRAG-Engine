from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from typing import Optional
import json

import requests

from backend.services.agent_orchestrator import orchestrate

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(
    question: str = Form(...),
    selected_pdfs: Optional[str] = Form(None),
    history: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    print("\n" + "=" * 60)
    print("MEDINTEL CHAT")
    print("=" * 60)
    print("Question:", question)
    
    # Convertir la chaîne en liste
    pdf_list = []
    if selected_pdfs and selected_pdfs.strip():
        try:
            pdf_list = json.loads(selected_pdfs)
        except:
            pdf_list = [selected_pdfs]
    
    try:
        # Appel à l'orchestrateur multi-agents
        result = orchestrate(question=question, pdf_names=pdf_list)
        
        return {
            "answer": result["answer"],
            "sources": result.get("sources", [])
        }
        
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Ollama is not running.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")