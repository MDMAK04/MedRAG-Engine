import os
import requests
from typing import Optional
from backend.services.retriever import retrieve
from backend.services.llm_service import generate_answer

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:7b"

def ask_medintel(question: str, selected_pdfs: list[str], history: Optional[str] = None):
    print("\n" + "=" * 60)
    print("MEDINTEL RAG")
    print("=" * 60)

    print("Question:", question)
    print("Selected PDFs:", selected_pdfs)

    results = retrieve(
        question=question,
        pdf_names=selected_pdfs,
    )

    if not results:
        return {
            "answer": ( "I could not find relevant information in the selected PDF documents."),
            "sources": [],
        }

    context_parts = []
    sources = []

    for result in results:
        text = result.get("text", "")
        file_name = result.get("file_name", "Unknown")
        page = result.get("page")
        context_parts.append(f"""
Source: {file_name}
Page: {page}
{text}
""")
        sources.append({
                "file_name": file_name,
                "page": page,
                "score": result.get(
                    "score"
                ),
            })
    context = "\n".join(context_parts)

    print("Sending context to Ollama...")
    answer = generate_answer(question, context)
    print("Ollama response received")

    return {
        "answer": answer,
        "sources": sources,
    }