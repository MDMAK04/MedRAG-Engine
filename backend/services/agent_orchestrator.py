import requests
import json
from pathlib import Path

# Configuration Ollama
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:7b"

from backend.services.llm_service import generate_answer
from backend.services.vision_agent import extract_images_from_pdf, analyze_image, analyze_single_image

def classify_question(question: str) -> str:
    prompt = f"""
You are an AI Supervisor. Classify the following user question into exactly one of these categories:
- 'RAG' : If the question requires information from specific documents or PDFs.
- 'VISION' : If the question asks about a specific image, graph, figure, or table.
- 'GENERAL' : If the question is a general conversation or medical knowledge question without needing documents.

Output ONLY the category name (RAG, VISION, or GENERAL). Nothing else.

User question:
{question}
"""
    try:
        category = generate_answer(question, prompt).upper().strip()
        
        if "VISION" in category:
            return "VISION"
        elif "RAG" in category:
            return "RAG"
        else:
            return "GENERAL"
    except:
        return "GENERAL"


def detect_vision_request(question: str) -> bool:
    vision_keywords = [
        "graphique", "figure", "image", "tableau", "courbe", "diagramme",
        "chart", "graph", "figure", "image", "table", "plot",
        "voir la page", "look at page", "radiographie", "x-ray", "mri", "scan",
        "regarde", "describe this image", "décris cette image", "décris"
    ]
    question_lower = question.lower()
    
    for keyword in vision_keywords:
        if keyword in question_lower:
            return True
    return False


def rag_agent(question: str, pdf_names: list) -> dict:
    from backend.services.retriever import retrieve_balanced
    
    pdf_names = [name.lower() for name in pdf_names]
    
    results = retrieve_balanced(question=question, pdf_names=pdf_names)
    
    context_parts = []
    
    for result in results:
        context_parts.append(
            f"FILE: {result.get('file_name')}, PAGE: {result.get('page')}\n{result.get('text', '')}"
        )
    
    context = "\n\n".join(context_parts) if context_parts else "No context retrieved."
    
    answer = generate_answer(question, context)
    
    return {
        "answer": answer,
        "sources": []
    }


def vision_agent(question: str, pdf_names: list, image_paths: list = None) -> dict:
    print(f"[AGENT] Executing Vision Agent...")
    
    context_text = ""
    if pdf_names:
        try:
            from backend.services.retriever import retrieve_balanced
            pdf_names_lower = [name.lower() for name in pdf_names]
            results = retrieve_balanced(question=question, pdf_names=pdf_names_lower)
            
            for result in results:
                context_text += f"Source: {result.get('file_name')}, Page: {result.get('page')}\n{result.get('text', '')}\n\n"
        except Exception as e:
            print(f"[VISION] Warning: Could not retrieve PDF context (Qdrant may be down): {e}")
            context_text = ""
    
    if image_paths and len(image_paths) > 0:
        print(f"[VISION] Analyzing single image: {image_paths[0]}")
        image_bytes = Path(image_paths[0]).read_bytes()
        
        answer = analyze_image(question, image_bytes, context_text)
        return {
            "answer": answer,
            "sources": [{
                "file_name": Path(image_paths[0]).name,
                "page": None,
                "score": 1.0
            }]
        }
    
    uploads_dir = Path("Data/uploads")
    pdf_paths = []
    
    for pdf_name in pdf_names:
        pdf_path = uploads_dir / pdf_name
        if pdf_path.exists():
            pdf_paths.append(pdf_path)
    
    if not pdf_paths:
        return {"answer": "No PDFs found for vision analysis.", "sources": []}
    
    all_images = []
    for pdf_path in pdf_paths:
        images = extract_images_from_pdf(str(pdf_path), max_images_per_page=3)
        for img in images:
            img["pdf_name"] = pdf_path.name
            all_images.append(img)
    
    if not all_images:
        return {"answer": "No images found in the selected documents.", "sources": []}
    
    target_image = all_images[0]
    print(f"[VISION] Analyzing image on page {target_image['page']} of {target_image['pdf_name']}")
    
    answer = analyze_image(question, target_image["image"], context_text)
    
    return {
        "answer": answer,
        "sources": [{
            "file_name": target_image["pdf_name"],
            "page": target_image["page"],
            "score": 1.0
        }]
    }


def general_agent(question: str) -> str:
    return generate_answer(question, "")


def orchestrate(question: str, pdf_names: list, image_paths: list = None) -> dict:
    print(f"\n[SUPERVISOR] Analyzing question: {question}")
    
    if detect_vision_request(question):
        print(f"[SUPERVISOR] Vision request detected via keywords!")
        print(f"[SUPERVISOR] {len(pdf_names)} PDF(s) detected! Forcing Vision Agent...")
        return vision_agent(question, pdf_names, image_paths)
    
    category = classify_question(question)
    print(f"[SUPERVISOR] Category selected: {category}")
    
    if category == "VISION":
        return vision_agent(question, pdf_names, image_paths)
    
    if pdf_names:
        print(f"[SUPERVISOR] {len(pdf_names)} PDF(s) detected! Forcing RAG Agent...")
        print(f"[AGENT] Executing RAG Agent...")
        return rag_agent(question, pdf_names)
    
    else:
        print(f"[AGENT] Executing General Agent...")
        answer = general_agent(question)
        return {"answer": answer, "sources": []}