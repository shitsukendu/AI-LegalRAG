from src.retriever import Retriever
from src.llm import ask_gemini
from src.citations import format_citations


class RAGPipeline:

    def __init__(self, top_k=3):
        self.retriever = Retriever(top_k=top_k)

    def answer_question(self, question, document_id=None):
        """
        Retrieve relevant legal document chunks,
        generate an answer using Gemini,
        and format source citations.

        If document_id is provided, retrieval is restricted
        to that specific document.
        """

        retrieved_chunks = self.retriever.retrieve(
            question,
            document_id=document_id
        )

        if not retrieved_chunks:
            return {
                "answer": (
                    "I could not find relevant information "
                    "in the document."
                ),
                "sources": [],
                "citations": []
            }

        context_parts = []

        for chunk in retrieved_chunks:

            page = chunk["page_number"]
            text = chunk["text"]

            context_parts.append(
                f"[Page {page}]\n{text}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are a legal document analysis assistant.

Your task is to answer the user's question
using ONLY the provided document context.

Do not invent or assume information.

If the answer cannot be found in the provided
context, clearly say that the information was
not found in the document.

Always mention the relevant page number(s).

This system provides document analysis only
and is not professional legal advice.

DOCUMENT CONTEXT:
-----------------
{context}
-----------------

USER QUESTION:
{question}

Answer clearly and concisely.
"""

        answer = ask_gemini(prompt)

        citations = format_citations(
            retrieved_chunks
        )

        return {
            "answer": answer,
            "sources": retrieved_chunks,
            "citations": citations
        }