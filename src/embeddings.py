import streamlit as st
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


@st.cache_resource
def load_embedding_model():
    """
    Load the embedding model only once.

    Streamlit reuses the same model across reruns,
    which improves application performance.
    """

    print(f"Loading embedding model: {MODEL_NAME}")

    return SentenceTransformer(MODEL_NAME)


class EmbeddingModel:

    def __init__(self):

        self.model = load_embedding_model()

    def embed_text(self, text):
        """
        Convert one text into an embedding vector.
        """

        return self.model.encode(
            text,
            normalize_embeddings=True
        )

    def embed_documents(self, texts):
        """
        Convert multiple texts into embedding vectors.
        """

        return self.model.encode(
            texts,
            normalize_embeddings=True
        )