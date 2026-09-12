import fitz


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF page by page.

    Returns:
        list: Each item contains page number and extracted text.
    """

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")

        if text.strip():
            pages.append(
                {
                    "page_number": page_number,
                    "text": text.strip(),
                }
            )

    document.close()

    return pages