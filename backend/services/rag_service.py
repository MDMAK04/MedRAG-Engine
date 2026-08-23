import os
import requests
from typing import Optional

from Scripts.retrieval.retriever import retrieve


# =========================================================
# CONFIGURATION OLLAMA (LOCAL)
# =========================================================

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:3b"


# =========================================================
# MEDINTEL RAG
# =========================================================

def ask_medintel(
    question: str,
    selected_pdfs: list[str],
    history: Optional[str] = None,
):

    print("\n" + "=" * 60)
    print("MEDINTEL RAG")
    print("=" * 60)

    print("Question:", question)
    print("Selected PDFs:", selected_pdfs)

    # -----------------------------------------------------
    # RETRIEVAL
    # -----------------------------------------------------

    results = retrieve(
        question=question,
        pdf_names=selected_pdfs,
    )

    if not results:

        return {
            "answer": (
                "I could not find relevant information "
                "in the selected PDF documents."
            ),
            "sources": [],
        }

    # -----------------------------------------------------
    # Build context
    # -----------------------------------------------------

    context_parts = []

    sources = []

    for result in results:

        text = result.get(
            "text",
            ""
        )

        file_name = result.get(
            "file_name",
            "Unknown"
        )

        page = result.get(
            "page"
        )

        context_parts.append(
            f"""
Source: {file_name}
Page: {page}

{text}
"""
        )

        sources.append(
            {
                "file_name": file_name,
                "page": page,
                "score": result.get(
                    "score"
                ),
            }
        )

    context = "\n".join(
        context_parts
    )

    # -----------------------------------------------------
    # Prompt
    # -----------------------------------------------------

    prompt = f"""
You are MedIntel-AI, a medical research assistant.

Answer the user's question using only the
retrieved information provided below.

Do not invent information.

If the retrieved information does not contain
the answer, say that the information was not
found in the selected documents.

Give a clear answer.

User question:
{question}

Retrieved medical evidence:
{context}
"""

    # -----------------------------------------------------
    # OLLAMA (LOCAL LLM) - PAS D'INTERNET REQUIS
    # -----------------------------------------------------

    print("Sending context to Ollama...")

    try:
        response = requests.post(
            url=f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120  # 2 minutes pour laisser le modèle local réfléchir
        )

        response.raise_for_status()

        data = response.json()
        
        answer = data.get("response", "").strip()

        if not answer:
            answer = "The local model did not generate an answer."

        print("Ollama response received")

    except requests.exceptions.ConnectionError:
        answer = "Unable to connect to Ollama. Please make sure Ollama is running (type 'ollama run qwen2.5:3b' in a terminal)."
    except Exception as e:
        answer = f"Error generating response: {str(e)}"

    return {
        "answer": answer,
        "sources": sources,
    }