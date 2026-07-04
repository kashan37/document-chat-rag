from src.loader import load_pdf
from src.chunker import chunk_text


PDF_PATH = "data/sample.pdf"

text, pages = load_pdf(PDF_PATH)

chunks = chunk_text(text)

print(f"Pages: {pages}")

print(f"Characters: {len(text)}")

print(f"Total Chunks: {len(chunks)}")

print()

for i, chunk in enumerate(chunks[:3]):

    print("=" * 60)

    print(f"Chunk {i+1}")

    print("=" * 60)

    print(chunk)

    print()