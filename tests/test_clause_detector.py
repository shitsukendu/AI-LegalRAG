from src.pdf_loader import extract_text_from_pdf
from src.clause_detector import detect_clauses


# Load PDF
pdf_path = "data/documents/sample_agreement.pdf"

pages = extract_text_from_pdf(pdf_path)


# Detect clauses
clauses = detect_clauses(pages)


print("\n" + "=" * 60)
print("IMPORTANT CLAUSE DETECTION")
print("=" * 60)

print("\n")
print(clauses)