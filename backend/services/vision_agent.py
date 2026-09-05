import pymupdf
import requests
import base64
from pathlib import Path

# Configuration
OLLAMA_URL = "http://localhost:11434"
VISION_MODEL = "llava:7b"

def extract_images_from_pdf(pdf_path: str, max_images_per_page: int = 2):
    doc = pymupdf.open(pdf_path)
    images = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        mat = pymupdf.Matrix(3, 3)
        pix = page.get_pixmap(matrix=mat)
        image_bytes = pix.tobytes("png")
        
        text = page.get_text("text")
        
        images.append({
            "page": page_num + 1,
            "image": image_bytes,
            "text": text
        })
    
    doc.close()
    return images

def encode_image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")

def analyze_image(question: str, image_bytes: bytes, context_text: str = "") -> str:
    image_base64 = encode_image_to_base64(image_bytes)

    prompt = f"""
You are a medical imaging assistant.
Analyze the image and answer the user's question.
Use the following medical context from a PDF to help you answer:

{context_text}

Answer in English.
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
        return response.json().get("response", "No response")
    except Exception as e:
        print(f"Vision model warning: {e}")
        return "The vision model is too slow or could not analyze the image."

def analyze_single_image(question: str, image_path: str) -> str:
    """
    ROLE : Analyse une image téléchargée directement (sans passer par un PDF).
    """
    image_bytes = Path(image_path).read_bytes()
    return analyze_image(question, image_bytes)