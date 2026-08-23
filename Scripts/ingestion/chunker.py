import re

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """
    Découpe le texte en chunks de taille moyenne avec un chevauchement.
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1  # +1 pour l'espace

        if current_length >= chunk_size:
            chunk_text = " ".join(current_chunk)
            if len(chunk_text.strip()) > 50: # Ignorer les chunks trop petits
                chunks.append(chunk_text)
            
            # Ajouter le chevauchement (overlap)
            overlap_words = current_chunk[-overlap:]
            current_chunk = overlap_words
            current_length = sum(len(w) + 1 for w in current_chunk)

    # Ajouter le dernier morceau
    if current_chunk:
        final_chunk = " ".join(current_chunk)
        if len(final_chunk.strip()) > 50:
            chunks.append(final_chunk)

    return chunks