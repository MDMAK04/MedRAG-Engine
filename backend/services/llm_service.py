import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


if not GEMINI_API_KEY:

    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


SYSTEM_INSTRUCTION = """
You are MedIntel-AI, a medical research assistant.

Answer the user's question using only the
scientific context provided to you.

Rules:

1. Use only the provided context.
2. Do not invent medical facts.
3. Do not use outside knowledge.
4. If the context is insufficient, say so clearly.
5. Give a direct and focused answer.
6. Combine information from multiple documents
   when relevant.
7. Do not mention Qdrant.
8. Do not mention embeddings.
9. Do not mention chunks.
10. Do not mention the RAG pipeline.
11. Do not create information that is not present
    in the retrieved documents.
12. Do not claim causation unless the documents
    explicitly support causation.
"""


def generate_answer(
    question: str,
    context: str
) -> str:

    prompt = f"""
{SYSTEM_INSTRUCTION}

Scientific context:

---------------- START CONTEXT ----------------

{context}

----------------- END CONTEXT -----------------

Question:

{question}

Answer using only the scientific context.
"""


    response = client.interactions.create(
        model=GEMINI_MODEL,
        input=prompt
    )


    if not response.output_text:

        return (
            "The model did not generate "
            "an answer."
        )


    return response.output_text.strip()