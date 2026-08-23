import os
import requests

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:3b"

SYSTEM_INSTRUCTION = """
You are MedIntel-AI, a medical research assistant.
Answer the user's question based on the provided scientific context.
Synthesize the information clearly.
If the context is completely unrelated to the question, state that the information was not found.
Do not invent medical facts. Do not mention RAG, Qdrant, embeddings, or chunks.
"""

def generate_answer(question: str, context: str) -> str:
    prompt = f"""
{SYSTEM_INSTRUCTION}

Scientific context:
---------------- START CONTEXT ----------------
{context}
----------------- END CONTEXT -----------------

Question:
{question}

Answer using the scientific context:
"""

    try:
        response = requests.post(
            url=f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        answer = data.get("response", "").strip()

        if not answer:
            return "The local model did not generate an answer."

        return answer

    except requests.exceptions.ConnectionError:
        return "Unable to connect to Ollama. Please make sure Ollama is running."
    except Exception as e:
        return f"Error generating response: {str(e)}"