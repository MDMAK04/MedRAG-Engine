import os
from typing import Optional

from dotenv import load_dotenv
from google import genai

from Scripts.retrieval.retriever import retrieve


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )


# =========================================================
# GEMINI
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)

MODEL_NAME = "gemini-2.5-flash"


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
    # Gemini
    # -----------------------------------------------------

    print("Sending context to Gemini...")

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    answer = response.text

    print("Gemini response received")

    return {
        "answer": answer,
        "sources": sources,
    }