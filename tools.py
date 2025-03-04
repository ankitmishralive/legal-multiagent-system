# tools.py
from crewai.tools import BaseTool
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from pydantic import ConfigDict
import os

class LegalRetrievalTool(BaseTool):
    name: str = "Legal Document Retrieval Tool"
    description: str = "Retrieves relevant sections from legal documents based on a query."

    pdf_paths: list
    db: FAISS  # The FAISS database

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _run(self, query: str) -> str:
        """Retrieves relevant sections from the legal documents."""
        results = self.db.similarity_search(query)
        return "\n\n".join([doc.page_content for doc in results])


def create_legal_db(pdf_paths, db_path="legal_db"):  # Added db_path
    """Loads, splits, and indexes PDF documents using FAISS."""
    if os.path.exists(db_path):
        print(f"Loading existing FAISS database from {db_path}")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  # Or another suitable model
        db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True) # Added allow_dangerous_deserialization
    else:
        print("Creating new FAISS database...")
        documents = []
        for path in pdf_paths:
            loader = PyPDFLoader(path)
            documents.extend(loader.load())

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_documents(documents)

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  # Or another suitable model

        db = FAISS.from_documents(texts, embeddings)
        db.save_local(db_path)  # Save the database to disk
        print(f"FAISS database saved to {db_path}")
    return db


# Initialize the vector database
pdf_paths = [
    "https://www.cyrilshroff.com/wp-content/uploads/2020/09/Guide-to-Litigation-in-India.pdf",
    "https://kb.icai.org/pdfs/PDFFile5b28c9ce64e524.54675199.pdf"
]

DB_PATH = "legal_db"  # Define a constant for the database path
legal_db = create_legal_db(pdf_paths, DB_PATH)  # Pass db_path
legal_retrieval_tool = LegalRetrievalTool(pdf_paths=pdf_paths, db=legal_db)  # Passes vector DB instance