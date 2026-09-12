from src.llm import ask_gemini


def detect_clauses(pages):
    """
    Detect important legal clauses from the document.
    """

    document_text = "\n\n".join(
        f"[Page {page['page_number']}]\n{page['text']}"
        for page in pages
    )

    prompt = f"""
You are a legal document intelligence assistant.

Analyze the document provided below and identify
the important clauses that are explicitly present
in the document.

Use ONLY the document content.
Do not invent clauses.

Look specifically for these categories:

1. Payment Terms
2. Confidentiality
3. Intellectual Property
4. Data Protection
5. AI-Related Terms
6. Limitation of Liability
7. Termination
8. Governing Law and Disputes
9. Notices
10. Warranties

For every clause that exists, provide:

- Clause name
- Short explanation
- Relevant page number

If a category is not present, do not invent it.

This is document analysis only and not professional
legal advice.

DOCUMENT:
-------------------------
{document_text}
-------------------------

Return the result in a clear numbered format.
"""

    result = ask_gemini(prompt)

    return result