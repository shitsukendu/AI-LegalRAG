from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text: str) -> str:
    """
    Basic text cleaning.
    Removes unnecessary spaces and blank lines.
    """
    if not text:
        return ""

    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    return "\n".join(lines)


def split_documents(pages, chunk_size=800, chunk_overlap=150):
    """
    Clean extracted PDF pages and split them into chunks.

    Each chunk keeps its original page number
    so that we can later show citations/sources.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    for page in pages:
        page_number = page["page_number"]
        text = clean_text(page["text"])

        if not text:
            continue

        page_chunks = splitter.split_text(text)

        for chunk in page_chunks:
            chunks.append({
                "text": chunk,
                "page_number": page_number
            })

    return chunks