import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .llm import get_embeddings_model

CHROMA_PERSIST_DIR = "./nexus_chroma_db"

def ingest_pdf(uploaded_file) -> str:
    """Ingests a PDF file into ChromaDB and returns a status message."""
    try:
        # Write to temp file because PyPDFLoader needs a file path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        loader = PyPDFLoader(tmp_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(documents)

        embeddings = get_embeddings_model()
        
        # Initialize or add to Chroma
        Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=CHROMA_PERSIST_DIR
        )
        
        os.unlink(tmp_path)
        return f"Successfully ingested {uploaded_file.name} ({len(splits)} chunks)."
    except Exception as e:
        return f"Error ingesting PDF: {str(e)}"

def get_retriever():
    """Returns a retriever interface for ChromaDB."""
    embeddings = get_embeddings_model()
    db = Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embeddings)
    return db.as_retriever(search_kwargs={"k": 4})
