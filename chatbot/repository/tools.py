def get_values(values):
    if values is None:
        return None
    return [dict(value) for value in values] if isinstance(values, list) else dict(values)


def bordering_text(text: str, chunk_size: int = 512) -> list[str]:

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    current_chunk = ""
    sentences = text.replace('\n', ' ').split('.')

    for sentence in sentences:
        sentence = sentence.strip() + '.'

        if len(current_chunk) + len(sentence) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            if current_chunk:
                current_chunk += ' '
            current_chunk += sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
