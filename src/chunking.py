def get_overlapping_chunks(text, chunk_size=5000, overlap=500):
    chunks = []
    if not text:
        return chunks
    
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
        if start >= len(text):
            break
    return chunks