from src.loader import load_pdf


PDF_PATH = "data/sample.pdf"

text, total_pages = load_pdf(PDF_PATH)

print("=" * 60)

print(f"Pages: {total_pages}")

print(f"Characters: {len(text)}")

print()

print("Preview:\n")

print(text[:1000])

print()

print("=" * 60)