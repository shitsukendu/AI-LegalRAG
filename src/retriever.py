from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore


class Retriever:

    def __init__(self, top_k=3):

        self.top_k = top_k

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore()

    def retrieve(self, query, document_id=None):
        """
        Retrieve the most relevant document chunks.

        If document_id is provided, retrieval is limited
        to that specific document.
        """

        query_embedding = self.embedding_model.embed_text(
            query
        )

        results = self.vector_store.search(
            query_embedding,
            top_k=self.top_k,
            document_id=document_id
        )

        retrieved_chunks = []

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        for i, document in enumerate(documents):

            retrieved_chunks.append({
                "text": document,
                "page_number": metadatas[i]["page_number"],
                "document_id": metadatas[i].get(
                    "document_id"
                ),
                "distance": distances[i]
            })

        return retrieved_chunks