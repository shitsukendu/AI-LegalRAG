from src.pdf_loader import extract_text_from_pdf
from src.retriever import Retriever
from src.citations import format_citations


# --------------------------------------------------
# 1. Create Retriever
# --------------------------------------------------

retriever = Retriever(top_k=3)


# --------------------------------------------------
# 2. Test Query
# --------------------------------------------------

query = "What is the termination period for convenience termination?"

print("\n" + "=" * 60)
print("CITATION TEST")
print("=" * 60)

print("\nQUERY:")
print(query)


# --------------------------------------------------
# 3. Retrieve Sources
# --------------------------------------------------

sources = retriever.retrieve(query)


print("\nRetrieved sources:", len(sources))


# --------------------------------------------------
# 4. Format Citations
# --------------------------------------------------

citations = format_citations(sources)


# --------------------------------------------------
# 5. Display Citations
# --------------------------------------------------

print("\n" + "=" * 60)
print("FORMATTED CITATIONS")
print("=" * 60)


for citation in citations:

    print("\n" + "-" * 60)

    print("REFERENCE:", citation["reference"])

    print("\nTEXT:")
    print(citation["text"])

    print("-" * 60)