from src.pdf_loader import extract_text_from_pdf
from src.summarizer import generate_summary


# Load PDF
pdf_path = "data/documents/sample_agreement.pdf"

pages = extract_text_from_pdf(pdf_path)


# Generate summary
summary = generate_summary(pages)


print("\n" + "=" * 60)
print("LEGAL DOCUMENT SUMMARY")
print("=" * 60)

print("\n")
print(summary)