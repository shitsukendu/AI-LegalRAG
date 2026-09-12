from src.retriever import Retriever


retriever = Retriever(top_k=3)


query = "What is the termination period for convenience termination?"


results = retriever.retrieve(query)


print("\n" + "=" * 60)
print("RAG RETRIEVAL TEST")
print("=" * 60)

print("Query:", query)

print("Retrieved chunks:", len(results))


for i, result in enumerate(results, start=1):

    print("\n" + "-" * 60)

    print(f"RESULT {i}")
    print("PAGE:", result["page_number"])
    print("DISTANCE:", result["distance"])

    print("-" * 60)

    print(result["text"])