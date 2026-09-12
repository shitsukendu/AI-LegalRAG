def format_citations(sources):
    """
    Format retrieved document sources into
    clean page-based citations.
    """

    if not sources:
        return []

    citations = []
    seen_pages = set()

    for source in sources:

        page = source.get("page_number")
        text = source.get("text", "")

        # Avoid duplicate page citations
        if page in seen_pages:
            continue

        seen_pages.add(page)

        citations.append({
            "page_number": page,
            "reference": f"Page {page}",
            "text": text
        })

    return citations