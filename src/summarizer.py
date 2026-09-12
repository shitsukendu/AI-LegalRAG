from src.llm import ask_gemini


def generate_summary(pages):
    """
    Generate a concise summary of the legal document.
    """

    # Combine all pages
    document_text = "\n\n".join(
        f"[Page {page['page_number']}]\n{page['text']}"
        for page in pages
    )

    prompt = f"""
You are a legal document analysis assistant.

Summarize the following document using ONLY
the information provided in the document.

Do not invent or assume any information.

Include:
1. Document purpose
2. Parties involved
3. Main services or obligations
4. Payment terms
5. Confidentiality
6. Intellectual property
7. Data protection
8. AI-related terms
9. Liability
10. Termination
11. Governing law and disputes

Mention page numbers when relevant.

This is document analysis only and not
professional legal advice.

DOCUMENT:
-------------------------
{document_text}
-------------------------

Write the summary in clear bullet points.
"""

    summary = ask_gemini(prompt)

    return summary