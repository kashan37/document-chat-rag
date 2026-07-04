from pypdf import PdfReader
import re


def load_pdf(pdf_path):
    """
    Reads a PDF and returns:
    1. Cleaned text
    2. Number of pages
    """

    reader = PdfReader(pdf_path)

    all_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            all_text += text + "\n"

    # Clean unnecessary whitespace
    all_text = clean_text(all_text)

    return all_text, len(reader.pages)


def clean_text(text):
    """
    Cleans extracted PDF text.
    """

    # Replace multiple spaces with one
    text = re.sub(r"\s+", " ", text)

    # Remove extra blank lines
    text = text.strip()

    return text