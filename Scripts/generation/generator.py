import ollama


MODEL_NAME = "qwen2.5:3b"


def build_history(history):

    messages = []

    if not history:
        return messages

    for message in history:

        if hasattr(message, "role"):

            role = message.role
            content = message.content

        elif isinstance(message, dict):

            role = message.get("role", "")
            content = message.get("content", "")

        else:

            continue

        if role and content:

            messages.append({
                "role": role,
                "content": content
            })

    return messages


def generate_answer(
    question,
    context,
    history=None
):

    conversation_history = build_history(history)

    if conversation_history:

        history_text = "\n\n".join(
            f"{message['role']}: {message['content']}"
            for message in conversation_history
        )

    else:

        history_text = "No previous conversation."


    prompt = f"""
You are MedIntel-AI, a medical research assistant.

Your task is to answer the user's question using only
the retrieved scientific context.

Rules:

1. Use only information explicitly supported by the retrieved context.

2. Do not invent medical facts.

3. Do not use information that is not present in the retrieved context.

4. Do not repeat the same information.

5. Do not repeat the same sentence.

6. Give each important finding only once.

7. If several retrieved chunks support the same finding,
   mention the finding only once.

8. Do not add a separate summary after the answer.

9. Do not repeat the conclusion at the end.

10. Keep the answer concise and clear.

11. Preserve important numerical values such as hazard ratios,
    confidence intervals, percentages and statistical results.

12. Do not use citations.

13. Do not use citation markers such as [1], [2], [3].

14. Do not refer to sources using numbers.

15. Answer directly without mentioning the retrieval process.

16. If the retrieved context does not contain enough information
    to answer the question, say that the information is not
    available in the provided scientific context.


Previous conversation:

{history_text}


Current question:

{question}


Retrieved scientific context:

{context}


Now answer the user's question.

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

    return response["message"]["content"].strip()