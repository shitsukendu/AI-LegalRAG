from src.llm import ask_gemini


def detect_risks(pages):
    """
    Detect potential review/attention areas
    in a legal document.

    This does NOT provide legal advice.
    """

    document_text = "\n\n".join(
        f"[Page {page['page_number']}]\n{page['text']}"
        for page in pages
    )

    prompt = f"""
You are a legal document intelligence assistant.

Analyze the document below and identify clauses
or provisions that may deserve additional human
review or attention.

IMPORTANT:
- Use ONLY information explicitly present in the document.
- Do not invent facts.
- Do not say that a clause is illegal, invalid, or definitely harmful.
- Do not provide professional legal advice.
- Describe items as "Attention Areas" or "Review Points".
- Explain why each item may deserve review based on the document.
- Include the relevant page number.

Focus on areas such as:
1. Payment obligations
2. Termination periods
3. Liability limitations
4. Confidentiality obligations
5. Intellectual property ownership
6. Data protection
7. AI-generated output limitations
8. Human review requirements
9. Dispute resolution
10. Notice requirements

For each Attention Area provide:

- Area
- Why it deserves attention
- Relevant document detail
- Page number

DOCUMENT:
-------------------------
{document_text}
-------------------------

Return the result in a clear numbered format.
"""

    result = ask_gemini(prompt)

    return result