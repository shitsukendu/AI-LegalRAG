import os
import tempfile
import hashlib
from datetime import datetime

import streamlit as st

from src.pdf_loader import extract_text_from_pdf
from src.text_splitter import split_documents
from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore
from src.rag_pipeline import RAGPipeline
from src.summarizer import generate_summary
from src.clause_detector import detect_clauses
from src.risk_detector import detect_risks


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="LegalRAG",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# Light + Dark Mode Friendly
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       Theme Variables
       -------------------------------------------------------- */

    :root {
        --bg: #f8fafc;
        --card: #ffffff;
        --text: #1e293b;
        --muted: #64748b;

        --blue: #60a5fa;
        --blue-light: #dbeafe;

        --purple: #a78bfa;
        --purple-light: #ede9fe;

        --green: #4ade80;
        --green-light: #dcfce7;

        --amber: #fbbf24;
        --amber-light: #fef3c7;

        --navy: #64748b;
        --border: #e2e8f0;
    }


    /* --------------------------------------------------------
       Main App
       -------------------------------------------------------- */

    .stApp {
        background-color: var(--bg);
        color: var(--text);
    }


    /* --------------------------------------------------------
       Main Content
       -------------------------------------------------------- */

    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.05rem;
        color: var(--muted);
        margin-bottom: 1.5rem;
    }


    /* --------------------------------------------------------
       Cards
       -------------------------------------------------------- */

    .info-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }


    .document-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
    }


    /* --------------------------------------------------------
       Section Headers
       -------------------------------------------------------- */

    .section-title {
        font-size: 1.4rem;
        font-weight: 650;
        color: var(--text);
    }


    /* --------------------------------------------------------
       Accent Labels
       -------------------------------------------------------- */

    .blue-label {
        background: var(--blue-light);
        color: #1d4ed8;
        padding: 0.35rem 0.7rem;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
    }


    .purple-label {
        background: var(--purple-light);
        color: #6d28d9;
        padding: 0.35rem 0.7rem;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
    }


    .green-label {
        background: var(--green-light);
        color: #15803d;
        padding: 0.35rem 0.7rem;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
    }


    .amber-label {
        background: var(--amber-light);
        color: #a16207;
        padding: 0.35rem 0.7rem;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
    }


    /* --------------------------------------------------------
       Sidebar
       -------------------------------------------------------- */

    [data-testid="stSidebar"] {
        border-right: 1px solid var(--border);
    }


    /* --------------------------------------------------------
       Buttons
       -------------------------------------------------------- */

    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 2.5rem;
    }


    /* --------------------------------------------------------
       File Uploader
       -------------------------------------------------------- */

    [data-testid="stFileUploader"] {
        background: var(--card);
        border-radius: 12px;
    }


    /* --------------------------------------------------------
       Dark Mode
       -------------------------------------------------------- */

    @media (prefers-color-scheme: dark) {

        :root {
            --bg: #111827;
            --card: #1f2937;
            --text: #f1f5f9;
            --muted: #cbd5e1;

            --blue-light: #1e3a5f;
            --purple-light: #34245c;
            --green-light: #173d29;
            --amber-light: #4a3914;

            --border: #374151;
        }

        .blue-label {
            color: #bfdbfe;
        }

        .purple-label {
            color: #ddd6fe;
        }

        .green-label {
            color: #bbf7d0;
        }

        .amber-label {
            color: #fde68a;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "history" not in st.session_state:
    st.session_state.history = []

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

if "document_id" not in st.session_state:
    st.session_state.document_id = None

if "pages" not in st.session_state:
    st.session_state.pages = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "analysis_ready" not in st.session_state:
    st.session_state.analysis_ready = False

if "summary" not in st.session_state:
    st.session_state.summary = None

if "clauses" not in st.session_state:
    st.session_state.clauses = None

if "attention_areas" not in st.session_state:
    st.session_state.attention_areas = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center; padding:10px 0 20px 0;">
            <div style="font-size:2rem;">⚖️</div>
            <div style="font-size:1.35rem; font-weight:700;">
                LegalRAG
            </div>
            <div style="font-size:0.85rem; opacity:0.75;">
                Legal Document Intelligence
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()


    # --------------------------------------------------------
    # Navigation
    # --------------------------------------------------------

    if st.button(
        "🏠  Home",
        use_container_width=True
    ):
        st.session_state.page = "Home"
        st.rerun()


    if st.button(
        "➕  New Document",
        use_container_width=True
    ):
        st.session_state.page = "New Document"

        st.session_state.uploaded_file_name = None
        st.session_state.pages = None
        st.session_state.chunks = None
        st.session_state.analysis_ready = False
        st.session_state.summary = None
        st.session_state.clauses = None
        st.session_state.attention_areas = None

        st.rerun()


    if st.button(
        "📚  History",
        use_container_width=True
    ):
        st.session_state.page = "History"
        st.rerun()


    st.divider()


    # --------------------------------------------------------
    # Recent Documents
    # --------------------------------------------------------

    st.markdown(
        "**📚 Recent Documents**"
    )

    if st.session_state.history:

        for item in reversed(
            st.session_state.history[-5:]
        ):

            st.markdown(
                f"""
                <div class="document-card">
                    📄 <b>{item['name']}</b><br>
                    <small>{item['time']}</small>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.caption(
            "No documents analyzed yet."
        )


    st.divider()

    st.caption(
        "LegalRAG • Educational Document Analysis"
    )


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "Home":

    st.markdown(
        '<div class="main-title">⚖️ LegalRAG</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
            AI-Powered Legal Document Intelligence & RAG Assistant
        </div>
        """,
        unsafe_allow_html=True
    )


    st.info(
        "This application provides document analysis for "
        "educational and informational purposes only. "
        "It is not professional legal advice."
    )


    # --------------------------------------------------------
    # Welcome Cards
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="info-card">
                <div class="blue-label">📄 Documents</div>
                <h3>Analyze PDFs</h3>
                <p>
                    Upload a legal document and analyze
                    its content using AI.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
            <div class="info-card">
                <div class="purple-label">🤖 AI Analysis</div>
                <h3>Understand Documents</h3>
                <p>
                    Generate summaries and identify
                    important clauses.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            """
            <div class="info-card">
                <div class="green-label">🔍 RAG</div>
                <h3>Ask Questions</h3>
                <p>
                    Ask questions and receive answers
                    grounded in the uploaded document.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.divider()

    st.markdown(
        '<div class="section-title">🚀 Get Started</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "➕ Upload a New Legal Document",
        use_container_width=True
    ):

        st.session_state.page = "New Document"
        st.rerun()


# ============================================================
# NEW DOCUMENT PAGE
# ============================================================

elif st.session_state.page == "New Document":

    st.markdown(
        '<div class="main-title">➕ New Legal Document</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Upload and analyze a legal PDF</div>',
        unsafe_allow_html=True
    )


    st.info(
        "Upload your PDF first. Document processing will begin "
        "only after you click the Analyze Document button."
    )


    # --------------------------------------------------------
    # PDF Upload
    # --------------------------------------------------------

    uploaded_file = st.file_uploader(
        "📄 Upload Legal Document",
        type=["pdf"],
        key="legal_pdf"
    )


    if uploaded_file is not None:

        st.success(
            f"Selected document: {uploaded_file.name}"
        )

        st.write(
            f"File size: "
            f"{uploaded_file.size / 1024:.2f} KB"
        )


        # ----------------------------------------------------
        # Analyze Button
        # ----------------------------------------------------

        st.divider()

        analyze_button = st.button(
            "🚀 Analyze Document",
            type="primary",
            use_container_width=True
        )

        if analyze_button:

            with st.spinner(
                "Analyzing document..."
            ):

                document_id = hashlib.md5(
                    uploaded_file.getvalue()
                ).hexdigest()[:12]

                temp_pdf_path = None
                

                try:

                    # ----------------------------------------
                    # Save temporary PDF
                    # ----------------------------------------

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as temp_file:

                        temp_file.write(
                            uploaded_file.getbuffer()
                        )

                        temp_pdf_path = temp_file.name


                    # ----------------------------------------
                    # Extract Text
                    # ----------------------------------------

                    st.write(
                        "📖 Extracting document text..."
                    )

                    pages = extract_text_from_pdf(
                        temp_pdf_path
                    )


                    # ----------------------------------------
                    # Create Chunks
                    # ----------------------------------------

                    st.write(
                        "✂️ Creating document chunks..."
                    )

                    chunks = split_documents(
                        pages,
                        chunk_size=800,
                        chunk_overlap=150
                    )


                    # ----------------------------------------
                    # Generate Embeddings
                    # ----------------------------------------

                    st.write(
                        "🧠 Generating embeddings..."
                    )

                    embedding_model = EmbeddingModel()

                    texts = [
                        chunk["text"]
                        for chunk in chunks
                    ]

                    embeddings = (
                        embedding_model.embed_documents(
                            texts
                        )
                    )


                    # ----------------------------------------
                    # ChromaDB
                    # ----------------------------------------

                    st.write(
                        "🗄️ Indexing document in ChromaDB..."
                    )

                    vector_store = VectorStore()

                    vector_store.add_chunks(
                        chunks,
                        embeddings,
                        document_id
                    )


                    # ----------------------------------------
                    # Save Session Data
                    # ----------------------------------------

                    st.session_state.pages = pages

                    st.session_state.chunks = chunks

                    st.session_state.uploaded_file_name = (
                        uploaded_file.name
                    )

                    st.session_state.document_id = document_id

                    st.session_state.analysis_ready = True

                    st.session_state.summary = None
                    st.session_state.clauses = None
                    st.session_state.attention_areas = None


                    # ----------------------------------------
                    # Add History
                    # ----------------------------------------

                    history_item = {
                        "name": uploaded_file.name,
                        "time": datetime.now().strftime(
                            "%d %b %Y, %I:%M %p"
                        )
                    }

                    st.session_state.history.append(
                        history_item
                    )


                    st.success(
                        "✅ Document analyzed successfully!"
                    )


                except Exception as e:

                    st.error(
                        f"Error processing document: {e}"
                    )


                finally:

                    if (
                        temp_pdf_path is not None
                        and os.path.exists(temp_pdf_path)
                    ):

                        os.remove(temp_pdf_path)


    # ========================================================
    # ANALYSIS RESULTS
    # ========================================================

    if st.session_state.analysis_ready:

        st.divider()


        # ----------------------------------------------------
        # Document Information
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">📊 Document Information</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "📄 Pages",
                len(st.session_state.pages)
            )

        with col2:

            st.metric(
                "✂️ Chunks",
                len(st.session_state.chunks)
            )

        with col3:

            st.metric(
                "🗂️ Status",
                "Indexed"
            )


        st.divider()


        # ----------------------------------------------------
        # TOP TABS
        # ----------------------------------------------------

        tab_summary, tab_clauses, tab_attention, tab_qa = st.tabs(
            [
                "📋 Summary",
                "📑 Important Clauses",
                "⚠️ Attention Areas",
                "🔍 Q&A"
            ]
        )


        # ====================================================
        # SUMMARY TAB
        # ====================================================

        with tab_summary:

            st.subheader(
                "📋 Document Summary"
            )

            if st.button(
                "✨ Generate Document Summary",
                use_container_width=True,
                key="summary_button"
            ):

                with st.spinner(
                    "Generating document summary..."
                ):

                    st.session_state.summary = (
                        generate_summary(
                            st.session_state.pages
                        )
                    )


            if st.session_state.summary:

                st.markdown(
                    "### 📝 AI Summary"
                )

                st.write(
                    st.session_state.summary
                )

            else:

                st.caption(
                    "Click the button above to generate an AI summary."
                )


        # ====================================================
        # CLAUSES TAB
        # ====================================================

        with tab_clauses:

            st.subheader(
                "📑 Important Clauses"
            )

            if st.button(
                "🔎 Detect Important Clauses",
                use_container_width=True,
                key="clauses_button"
            ):

                with st.spinner(
                    "Analyzing important clauses..."
                ):

                    st.session_state.clauses = (
                        detect_clauses(
                            st.session_state.pages
                        )
                    )


            if st.session_state.clauses:

                st.markdown(
                    "### 📑 Detected Clauses"
                )

                st.write(
                    st.session_state.clauses
                )

            else:

                st.caption(
                    "Click the button above to detect important clauses."
                )


        # ====================================================
        # ATTENTION AREAS TAB
        # ====================================================

        with tab_attention:

            st.subheader(
                "⚠️ Attention Areas"
            )

            st.warning(
                "These are document-based review points only. "
                "They are not professional legal advice."
            )


            if st.button(
                "⚠️ Detect Attention Areas",
                use_container_width=True,
                key="attention_button"
            ):

                with st.spinner(
                    "Analyzing document attention areas..."
                ):

                    st.session_state.attention_areas = (
                        detect_risks(
                            st.session_state.pages
                        )
                    )


            if st.session_state.attention_areas:

                st.markdown(
                    "### 🔎 Document Review Points"
                )

                st.write(
                    st.session_state.attention_areas
                )

            else:

                st.caption(
                    "Click the button above to detect review points."
                )


        # ====================================================
        # Q&A TAB
        # ====================================================

        with tab_qa:

            st.subheader(
                "🔍 Ask Questions About Your Document"
            )

            st.caption(
                "Answers are generated using the indexed document."
            )


            question = st.text_input(
                "Enter your question",
                placeholder=(
                    "Example: What is the termination period?"
                ),
                key="question_input"
            )


            ask_button = st.button(
                "💬 Ask Question",
                type="primary",
                use_container_width=True,
                key="ask_button"
            )


            if ask_button:

                if not question.strip():

                    st.warning(
                        "Please enter a question."
                    )

                else:

                    with st.spinner(
                        "Searching document and generating answer..."
                    ):

                        rag = RAGPipeline(
                            top_k=3
                        )

                        result = rag.answer_question(
                            question,
                        document_id=st.session_state.document_id
                        )


                    st.markdown(
                        "### 💬 Answer"
                    )

                    st.write(
                        result["answer"]
                    )


                    st.markdown(
                        "### 📚 Sources / Citations"
                    )


                    citations = result.get(
                        "citations",
                        []
                    )


                    if citations:

                        for citation in citations:

                            with st.expander(
                                citation["reference"]
                            ):

                                st.write(
                                    citation["text"]
                                )

                    else:

                        st.caption(
                            "No sources found."
                        )


        # ----------------------------------------------------
        # Extracted Text
        # ----------------------------------------------------

        st.divider()

        with st.expander(
            "📄 View Extracted Document Text"
        ):

            for page in st.session_state.pages:

                st.markdown(
                    f"### Page {page['page_number']}"
                )

                st.write(
                    page["text"]
                )


# ============================================================
# HISTORY PAGE
# ============================================================

elif st.session_state.page == "History":

    st.markdown(
        '<div class="main-title">📚 Document History</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Recently analyzed documents</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.history:

        st.info(
            "No documents have been analyzed yet."
        )

    else:

        for index, item in enumerate(
            reversed(st.session_state.history),
            start=1
        ):

            st.markdown(
                f"### 📄 Document {index}"
            )

            st.markdown(
                f"**📑 {item['name']}**"
            )

            st.caption(
                f"🕒 Analyzed on {item['time']}"
            )

            st.divider()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "⚖️ LegalRAG — AI-Powered Legal Document Intelligence | "
    "For educational and informational purposes only."
)