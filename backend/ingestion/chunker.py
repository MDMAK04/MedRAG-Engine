import re

def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 120) -> list:
    """
    Découpe un texte en morceaux (chunks) de taille fixe avec un chevauchement.
    """
    if not text:
        return []
    
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        word_len = len(word) + 1  
        if current_length + word_len > chunk_size:
            # Sauvegarder le chunk actuel
            chunks.append(" ".join(current_chunk))
            
            # Appliquer le chevauchement : garder les derniers mots
            overlap_words = current_chunk[-chunk_overlap:] if chunk_overlap > 0 else []
            current_chunk = overlap_words + [word]
            current_length = sum(len(w) + 1 for w in current_chunk)
        else:
            current_chunk.append(word)
            current_length += word_len
    
    # Ajouter le dernier chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks