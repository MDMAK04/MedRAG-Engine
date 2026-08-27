import pymupdf
import requests
import base64
from pathlib import Path

# Configuration
OLLAMA_URL = "http://localhost:11434"
VISION_MODEL = "llava:7b"
TEXT_MODEL = "qwen2.5:7b"  # Pour comprendre le texte


def extract_images_from_pdf(pdf_path: str, max_images_per_page: int = 2):
    doc = pymupdf.open(pdf_path)
    images = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        mat = pymupdf.Matrix(3, 3)
        pix = page.get_pixmap(matrix=mat)
        image_bytes = pix.tobytes("png")
        
        # Extraire aussi le texte de la page (pour le contexte)
        text = page.get_text("text")
        
        images.append({
            "page": page_num + 1,
            "image": image_bytes,
            "text": text  # 🔥 AJOUT DU TEXTE
        })
    
    doc.close()
    return images


def encode_image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def analyze_image(question: str, image_bytes: bytes, page_text: str = "") -> str:
    image_base64 = encode_image_to_base64(image_bytes)
    
    # 🔥 ASTUCE : On met le texte de la page dans le prompt pour guider le modèle
    prompt = f"""
You are a medical imaging assistant analyzing a graph from a scientific paper.
The following text is extracted from the SAME page as the graph (use this to guide you):

Page Text:
{page_text[:1000]}  # On limite à 1000 caractères pour ne pas surcharger

Now, analyze the provided image (the graph) and answer the user's question.
Answer in English. Be precise about the X-axis, Y-axis, and any trends.

Question: {question}
"""
    
    try:
        response = requests.post(
            url=f"{OLLAMA_URL}/api/generate",
            json={
                "model": VISION_MODEL,
                "prompt": prompt,
                "images": [image_base64],
                "stream": False
            },
            timeout=300
        )
        response.raise_for_status()
        return response.json().get("response", "No response from vision model.")
    except Exception as e:
        print(f"Vision model warning: {e}")
        return "The vision model is too slow or could not analyze the image due to system constraints."