def chunk_text(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 120
):

    if not text or not text.strip():
        return []

    words = text.split()

    chunks = []

    current_chunk = []
    current_length = 0

    for word in words:

        word_length = len(word) + 1

        if (
            current_length + word_length > chunk_size
            and current_chunk
        ):

            chunks.append(
                " ".join(current_chunk)
            )

            overlap_words = []
            overlap_length = 0

            for previous_word in reversed(current_chunk):

                if (
                    overlap_length
                    + len(previous_word)
                    + 1
                    > chunk_overlap
                ):
                    break

                overlap_words.insert(
                    0,
                    previous_word
                )

                overlap_length += (
                    len(previous_word) + 1
                )

            current_chunk = overlap_words
            current_length = overlap_length

        current_chunk.append(word)
        current_length += word_length

    if current_chunk:

        chunks.append(
            " ".join(current_chunk)
        )

    return chunks