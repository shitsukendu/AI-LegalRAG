import chromadb


class VectorStore:

    def __init__(self, collection_name="legal_documents"):

        self.client = chromadb.PersistentClient(
            path="data/vector_db"
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_chunks(self, chunks, embeddings, document_id):
        """
        Store document chunks, embeddings,
        page metadata, and document ID.
        """

        documents = []
        ids = []
        metadatas = []

        for i, chunk in enumerate(chunks):

            documents.append(
                chunk["text"]
            )

            # Unique ID for each document's chunk
            ids.append(
                f"{document_id}_chunk_{i}"
            )

            metadatas.append({
                "page_number": chunk["page_number"],
                "document_id": document_id
            })

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

        print(
            f"Stored {len(chunks)} chunks "
            f"for document: {document_id}"
        )

    def search(
        self,
        query_embedding,
        top_k=3,
        document_id=None
    ):
        """
        Search for relevant chunks.

        If document_id is provided,
        search only inside that document.
        """

        query_params = {
            "query_embeddings": [
                query_embedding.tolist()
            ],
            "n_results": top_k,
            "include": [
                "documents",
                "metadatas",
                "distances"
            ]
        }

        if document_id:
            query_params["where"] = {
                "document_id": document_id
            }

        results = self.collection.query(
            **query_params
        )

        return results