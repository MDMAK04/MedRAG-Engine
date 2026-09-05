from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import Filter, FieldCondition, MatchAny

COLLECTION_NAME = "medical_articles"
QDRANT_URL = "http://localhost:6333"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5

print("Initializing Qdrant...")
client = QdrantClient(url=QDRANT_URL)
print("Qdrant connected")

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)
print("Embedding model loaded")


def create_question_embedding(question: str):
    print("Creating question embedding...")
    embedding = model.encode(
        question,
        normalize_embeddings=True
    )
    print("Question embedding created")
    return embedding.tolist()

def retrieve_chunks(question_embedding, selected_pdfs=None):
    print("Searching Qdrant...")
    query_filter = None

    if selected_pdfs:
        print("Filtering by PDFs:", selected_pdfs)
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="filename",
                    match=MatchAny(
                        any=selected_pdfs
                    )
                )
            ]
        )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_embedding,
        query_filter=query_filter,
        limit=TOP_K,
        with_payload=True
    ).points

    print(f"Qdrant returned {len(results)} chunks")
    return results


def retrieve(question, selected_pdfs=None):
    question_embedding = create_question_embedding(question)
    results = retrieve_chunks(question_embedding, selected_pdfs)

    return results