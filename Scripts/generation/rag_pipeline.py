from pathlib import Path
import sys


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]


# Allow imports from Scripts/retrieval
sys.path.append(
    str(PROJECT_ROOT / "Scripts" / "retrieval")
)


# Allow imports from Scripts/generation
sys.path.append(
    str(PROJECT_ROOT / "Scripts" / "generation")
)


from retriever import retrieve
from context_builder import build_context
from generator import generate_answer


def run_rag(question):
    """
    Complete RAG pipeline.

    1. Retrieve relevant chunks from Qdrant
    2. Build the context
    3. Generate the final answer with Ollama
    """

    print("Question:")
    print(question)

    # ==========================================
    # STEP 1: RETRIEVAL
    # ==========================================

    print()
    print("Step 1: Retrieval")

    results = retrieve(question)

    print(f"Retrieved chunks: {len(results)}")

    # ==========================================
    # STEP 2: CONTEXT BUILDING
    # ==========================================

    print()
    print("Step 2: Context building")

    context = build_context(results)

    print("Context built successfully")

    # ==========================================
    # STEP 3: GENERATION
    # ==========================================

    print()
    print("Step 3: Generation")

    answer = generate_answer(
        question,
        context
    )

    # ==========================================
    # FINAL ANSWER
    # ==========================================

    print()
    print("==============================")
    print("FINAL ANSWER")
    print("==============================")
    print()

    print(answer)


if __name__ == "__main__":

    question = (
        "What is the association between family history "
        "of stroke and ischemic stroke risk?"
    )

    run_rag(question)