import json
from pathlib import Path

from Scripts.retrieval.retriever import retrieve


BASE_DIR = Path(__file__).resolve().parents[2]

QUESTIONS_FILE = BASE_DIR / "Data" / "evaluation" / "questions.json"

TOP_K = 5


def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_question(question_data):

    question_id = question_data["id"]
    question = question_data["question"]

    print()
    print("=" * 70)
    print(f"{question_id}")
    print("=" * 70)

    print(f"Question: {question}")

    print()
    print("Retrieving...")

    results = retrieve(question)

    print(f"Retrieved: {len(results)} chunks")

    print()
    print("-" * 70)

    for rank, result in enumerate(results, start=1):

        payload = result.payload

        chunk_id = payload.get("chunk_id")
        pmcid = payload.get("pmcid")
        path = payload.get("path")
        text = payload.get("text", "")

        print()
        print(f"Rank: {rank}")
        print(f"Score: {result.score:.4f}")
        print(f"Chunk ID: {chunk_id}")
        print(f"PMCID: {pmcid}")
        print(f"Path: {path}")

        print()
        print("Text:")
        print(text[:500])

        print()
        print("-" * 70)


def main():

    print("=" * 70)
    print("MEDINTEL-AI RETRIEVAL EVALUATION")
    print("=" * 70)

    questions = load_questions()

    print(f"Questions: {len(questions)}")

    for question_data in questions:
        evaluate_question(question_data)

    print()
    print("=" * 70)
    print("RETRIEVAL EVALUATION FINISHED")
    print("=" * 70)


if __name__ == "__main__":
    main()