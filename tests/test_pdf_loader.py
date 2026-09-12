from src.pdf_loader import extract_text_from_pdf


pdf_path = "data/documents/sample_agreement.pdf"

pages = extract_text_from_pdf(pdf_path)

print("\nPDF successfully loaded!")
print("Total pages extracted:", len(pages))

for page in pages[:2]:
    print("\n" + "=" * 60)
    print("PAGE:", page["page_number"])
    print("=" * 60)
    print(page["text"][:1000])