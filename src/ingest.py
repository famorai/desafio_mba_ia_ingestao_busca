import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_ollama import OllamaEmbeddings

load_dotenv()

PGVECTOR_URL = os.getenv("PGVECTOR_URL")
OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL")
OLLAMA_EMBEDDING_MODEL=os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")

COLLECTION = "ollama_collection"

def main():

    loader = PyPDFLoader(os.getenv("PDF_PATH", "desafio_doc.pdf"))
    docs = loader.load()

    print("Pages:", len(docs))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(docs)

    print("Chunks:", len(chunks))

    embeddings = OllamaEmbeddings(
        model=OLLAMA_EMBEDDING_MODEL,
        base_url=OLLAMA_BASE
    )

    vector_store = PGVector(
        embeddings=embeddings,
        connection=PGVECTOR_URL,
        collection_name=COLLECTION
    )

    vector_store.add_documents(chunks)

    print("Ingestion completed!")

if __name__ == "__main__":
    main()