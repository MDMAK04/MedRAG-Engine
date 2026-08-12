import json
import sys
from pathlib import Path
from datetime import datetime


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(PROJECT_ROOT / "Scripts" / "retrieval")
)

sys.path.append(
    str(PROJECT_ROOT / "Scripts" / "generation")
)


# ============================================================
# IMPORT RAG COMPONENTS
# ============================================================

from retriever import retrieve
from context_builder import build_context
from generator import generate_answer


# ============================================================
# PATHS
# ============================================================

QUESTIONS_FILE = (
    PROJECT_ROOT
    / "Data"
    / "evaluation"
    / "questions.json"
)

RESULTS_DIR = (
    PROJECT_ROOT
    / "Data"
    / "evaluation"
    / "results"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD QUESTIONS
# ============================================================

with open(
    QUESTIONS_FILE,
    "r",
    encoding="utf-8"
) as f:

    questions = json.load(f)


print("=" * 70)
print("MEDINTEL-AI RAG EVALUATION")
print("=" * 70)

print(f"Questions: {len(questions)}")
print()


# ============================================================
# EVALUATION
# ============================================================

evaluation_results = []

for index, item in enumerate(questions, start=1):

    question_id = item["id"]
    question = item["question"]

    print("=" * 70)
    print(f"QUESTION {index}/{len(questions)}")
    print(f"ID: {question_id}")
    print("=" * 70)

    print()
    print("Question:")
    print(question)

    # --------------------------------------------------------
    # Retrieval
    # --------------------------------------------------------

    print()
    print("Retrieval...")

    results = retrieve(question)

    print(
        f"Retrieved chunks: {len(results)}"
    )

    # --------------------------------------------------------
    # Context
    # --------------------------------------------------------

    context = build_context(results)

    # --------------------------------------------------------
    # Generation
    # --------------------------------------------------------

    print("Generation...")

    answer = generate_answer(
        question,
        context
    )

    # --------------------------------------------------------
    # Retrieved sources
    # --------------------------------------------------------

    sources = []

    for rank, result in enumerate(
        results,
        start=1
    ):

        payload = result.payload

        sources.append(
            {
                "rank": rank,
                "pmcid": payload.get(
                    "pmcid",
                    "Unknown"
                ),
                "section": payload.get(
                    "path",
                    "Unknown"
                ),
                "chunk_id": payload.get(
                    "chunk_id",
                    "Unknown"
                ),
                "score": result.score
            }
        )

    # --------------------------------------------------------
    # Store result
    # --------------------------------------------------------

    evaluation_results.append(
        {
            "id": question_id,
            "question": question,
            "answer": answer,
            "retrieved_chunks": len(results),
            "sources": sources
        }
    )

    print()
    print("Answer:")
    print(answer)

    print()


# ============================================================
# SAVE RESULTS
# ============================================================

timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

output_file = (
    RESULTS_DIR
    / f"evaluation_{timestamp}.json"
)


with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        evaluation_results,
        f,
        indent=4,
        ensure_ascii=False
    )


print("=" * 70)
print("EVALUATION FINISHED")
print("=" * 70)

print()
print(
    f"Results saved to:\n{output_file}"
)