from pathlib import Path
import sys

# Permet d'importer retriever.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "Scripts" / "retrieval"))

from retriever import retrieve

def build_context(results):
    """
    Transforme les résultats de Qdrant
    en contexte texte utilisable par un LLM.
    """
    context_parts = []
    for rank, result in enumerate(results, start=1):
        payload = result.payload
        pmcid = payload.get("pmcid", "Unknown")
        path = payload.get("path", "Unknown")
        chunk_id = payload.get("chunk_id", "Unknown")
        text = payload.get("text", "")

        context_part = f"""
SOURCE {rank}

PMCID: {pmcid}
SECTION: {path}
CHUNK ID: {chunk_id}
SIMILARITY SCORE: {result.score:.4f}

TEXT:
{text}
"""

        context_parts.append(context_part.strip())

    return "\n\n" + "\n\n".join(context_parts)


def main():

    question = (
        "What is the association between family history "
        "of stroke and ischemic stroke risk?"
    )

    print("Question:")
    print(question)

    print()
    print("Retrieving relevant chunks...")

    results = retrieve(question)

    print(f"Retrieved chunks: {len(results)}")

    print()
    print("Building context...")

    context = build_context(results)

    print("Context built successfully")

    print()
    print("==============================")
    print("GENERATED CONTEXT")
    print("==============================")

    print(context)


if __name__ == "__main__":
    main()