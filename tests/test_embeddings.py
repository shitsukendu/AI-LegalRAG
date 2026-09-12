from src.pdf_loader import extract_text_from_pdf
from src.text_splitter import split_documents
from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore


# --------------------------------------------------
# 1. PDF
# --------------------------------------------------

pdf_path = "data/documents/sample_agreement.pdf"

pages = extract_text_from_pdf(pdf_path)

print("\nPDF pages:", len(pages))


# --------------------------------------------------
# 2. Chunking
# --------------------------------------------------

chunks = split_documents(
    pages,
    chunk_size=800,
    chunk_overlap=150
)

print("Total chunks:", len(chunks))


# --------------------------------------------------
# 3. Embedding Model
# --------------------------------------------------

embedding_model = EmbeddingModel()


texts = [
    chunk["text"]
    for chunk in chunks
]


# --------------------------------------------------
# 4. Generate Embeddings
# --------------------------------------------------

embeddings = embedding_model.embed_documents(
    texts
)

print(
    "Embedding shape:",
    embeddings.shape
)


# --------------------------------------------------
# 5. Store in Vector Database
# --------------------------------------------------

vector_store = VectorStore()

vector_store.add_chunks(
    chunks,
    embeddings
)


# --------------------------------------------------
# 6. Semantic Search Test
# --------------------------------------------------

query = "What is the termination period?"

print("\nQuery:", query)


query_embedding = embedding_model.embed_text(
    query
)


results = vector_store.search(
    query_embedding,
    top_k=3
)


# --------------------------------------------------
# 7. Display Results
# --------------------------------------------------

print("\n" + "=" * 60)
print("SEMANTIC SEARCH RESULTS")
print("=" * 60)


for i, document in enumerate(
    results["documents"][0],
    start=1
):

    page = results["metadatas"][0][i - 1]["page_number"]

    distance = results["distances"][0][i - 1]

    print("\n" + "-" * 60)

    print(f"RESULT {i}")
    print(f"PAGE: {page}")
    print(f"DISTANCE: {distance}")

    print("-" * 60)

    print(document)