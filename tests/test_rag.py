from src.rag_pipeline import RAGPipeline


# --------------------------------------------------
# 1. Create RAG Pipeline
# --------------------------------------------------

rag = RAGPipeline(top_k=3)


# --------------------------------------------------
# 2. Test Question
# --------------------------------------------------

question = (
    "What is the termination period "
    "for convenience termination?"
)


# --------------------------------------------------
# 3. Get Answer
# --------------------------------------------------

result = rag.answer_question(question)


# --------------------------------------------------
# 4. Display Answer
# --------------------------------------------------

print("\n" + "=" * 60)
print("LEGAL RAG + CITATION TEST")
print("=" * 60)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(result["answer"])


# --------------------------------------------------
# 5. Display Citations
# --------------------------------------------------

print("\n" + "=" * 60)
print("CITATIONS")
print("=" * 60)


for citation in result["citations"]:

    print("\n" + "-" * 60)

    print("REFERENCE:")
    print(citation["reference"])

    print("\nSOURCE TEXT:")
    print(citation["text"])

    print("-" * 60)