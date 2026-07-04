def chunk_text(text, chunk_size=500, overlap=100):
    """
    Split text into overlapping chunks.

    Parameters:
        text (str): Complete document text.
        chunk_size (int): Number of characters per chunk.
        overlap (int): Number of overlapping characters.

    Returns:
        list: List of text chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks