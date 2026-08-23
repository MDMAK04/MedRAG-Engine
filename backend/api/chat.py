from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from typing import Optional, List
import requests
import json

# Import du retriever
try:
    from Scripts.retrieval.retriever import retrieve
except Exception as e:
    print(f"CRITICAL: Error importing retriever: {e}")
    retrieve = None

router = APIRouter()

# Configuration Ollama (Local)
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:7b"


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
    
    # =========================================================
    # BLINDAGE : Convertir la chaîne des PDFs en liste
    # =========================================================
    pdf_list = []
    if selected_pdfs:
        if selected_pdfs.strip():  # Si ce n'est pas une chaîne vide
            try:
                pdf_list = json.loads(selected_pdfs)
            except:
                pdf_list = [selected_pdfs]
    
    print("Selected PDFs:", pdf_list)

    # =========================================================
    # 1. DÉCISION : MODE RAG (avec PDF) ou MODE CHAT (sans PDF)
    # =========================================================
    
    if pdf_list and retrieve is not None:
        try:
            results = retrieve(question=question, pdf_names=pdf_list)
            
            context_parts = []
            sources = []
            for result in results:
                context_parts.append(
                    f"Source: {result.get('file_name')}, Page: {result.get('page')}\n{result.get('text')}"
                )
                sources.append({
                    "file_name": result.get("file_name"),
                    "page": result.get("page"),
                    "score": result.get("score")
                })
            
            context = "\n\n".join(context_parts) if context_parts else "No context retrieved."
            
            prompt = f"""
You are MedIntel-AI, a medical research assistant.
Answer the user's question using ONLY the retrieved information provided below.
ALWAYS ANSWER IN ENGLISH.
Do not invent information.
If the retrieved information does not contain the answer, say that the information was not found in the selected documents.

User question:
{question}

Retrieved medical evidence:
{context}
"""
        except Exception as e:
            print(f"Warning: Could not retrieve context from Qdrant: {e}")
            context = "No context retrieved."
            sources = []
            prompt = f"Answer this medical question in English: {question}"
            
    else:
        # ✅ MODE CONVERSATION GÉNÉRALE (Sans PDF)
        print("No PDF selected, switching to general chat mode...")
        sources = []
        prompt = f"""
You are MedIntel-AI, a helpful medical research assistant.
Answer the user's question concisely and accurately.
ALWAYS ANSWER IN ENGLISH.

User question:
{question}
"""

    # =========================================================
    # 2. APPEL À OLLAMA (LOCAL)
    # =========================================================
    try:
        print("Sending context to Ollama...")
        response = requests.post(
            url=f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )
        response.raise_for_status()
        answer = response.json().get("response", "No response")
        print("Ollama response received")
        
        return {"answer": answer, "sources": sources}  

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Ollama is not running. Please run 'ollama run qwen2.5:7b' in a terminal.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")