from src.pdf_loader import extract_text_from_pdf
from src.text_splitter import split_documents


pdf_path = "data/documents/sample_agreement.pdf"

pages = extract_text_from_pdf(pdf_path)

chunks = split_documents(
    pages,
    chunk_size=800,
    chunk_overlap=150
)

print("\n" + "=" * 60)
print("TEXT CHUNKING SUCCESSFUL")
print("=" * 60)

print("Total pages:", len(pages))
print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks[:5], start=1):
    print("\n" + "-" * 60)
    print("CHUNK:", i)
    print("PAGE:", chunk["page_number"])
    print("-" * 60)
    print(chunk["text"])