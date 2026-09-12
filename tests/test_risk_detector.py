from src.pdf_loader import extract_text_from_pdf
from src.risk_detector import detect_risks


# Load PDF
pdf_path = "data/documents/sample_agreement.pdf"

pages = extract_text_from_pdf(pdf_path)


# Detect attention areas
risks = detect_risks(pages)


print("\n" + "=" * 60)
print("LEGAL DOCUMENT ATTENTION AREAS")
print("=" * 60)

print("\n")
print(risks)