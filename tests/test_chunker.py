from backend.services.chunker import chunk_text

def test_chunk_text_returns_chunks():
    text = "This is a medical document about atrial fibrillation. " * 100

    chunks = chunk_text(
        text,
        chunk_size=800,
        chunk_overlap=120
    )

    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)
    assert all(chunk.strip() for chunk in chunks)