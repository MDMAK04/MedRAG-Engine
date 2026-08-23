import pymupdf
import re

def clean_extracted_text(text: str) -> str:
    # 1. Supprime les caractères non-ASCII (comme les caractères chinois parasites)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # 2. Remplace les sauts de ligne et espaces multiples par un seul espace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_pages_from_pdf(pdf_path: str):
    document = pymupdf.open(pdf_path)
    pages = []

    for page_number, page in enumerate(document, start=1):
        # Extraction brute
        raw_text = page.get_text("text").strip()
        
        # Nettoyage agressif
        text = clean_extracted_text(raw_text)

        if not text:
            continue

        pages.append({
            "page": page_number,
            "text": text
        })

    document.close()
    return pages

def extract_text_from_pdf(pdf_path: str) -> str:
    pages = extract_pages_from_pdf(pdf_path)
    return "\n\n".join(
        f"PAGE {page['page']}\n\n{page['text']}"
        for page in pages
    )