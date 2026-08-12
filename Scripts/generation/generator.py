import ollama


MODEL_NAME = "llama3.2"


def generate_answer(question, context):

    prompt = f"""
You are a medical research assistant.

Answer the user's question using only the provided context.

If the context does not contain enough information,
say that the information is not available in the provided sources.

Do not invent facts.

Question:
{question}

Context:
{context}

Answer:
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]