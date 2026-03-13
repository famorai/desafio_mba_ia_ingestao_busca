import os
import sys
from dotenv import load_dotenv


from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

# ─── Configuração ────────────────────────────────────────────────────────────

load_dotenv()

PGVECTOR_URL = os.getenv("PGVECTOR_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
OLLAMA_BASE  = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
COLLECTION   = os.getenv("PGVECTOR_COLLECTION", "ollama_collection")

# ─── Funções públicas ─────────────────────────────────────────────────────────

def get_vectorstore() -> PGVector:
    """Conecta ao pgVector e retorna o vectorstore pronto para busca."""
    if not PGVECTOR_URL:
        print("[ERRO] Variável PGVECTOR_URL não definida no .env")
        sys.exit(1)

    embeddings = OllamaEmbeddings(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE,
    )

    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION,
        connection=PGVECTOR_URL,
        use_jsonb=True,
    )
    return vectorstore


def search(query: str, k: int = 10) -> list[tuple]:
    """
    Realiza busca semântica por similaridade.

    Parâmetros:
        query: pergunta do usuário (texto).
        k:     número de resultados a retornar.

    Retorna:
        Lista de tuplas (Document, score).
    """
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search_with_score(query, k=k)
    return results


def get_context(query: str, k: int = 10) -> str:
    """
    Retorna o contexto concatenado dos k chunks mais relevantes.
    Pronto para ser inserido no prompt da LLM.
    """
    results = search(query, k=k)
    if not results:
        return ""

    pieces = []
    for doc, score in results:
        pieces.append(doc.page_content)

    return "\n\n---\n\n".join(pieces)


# ─── Teste rápido via CLI ─────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python src/search.py 'sua pergunta aqui'")
        sys.exit(1)

    query = sys.argv[1]
    print(f"\n[BUSCA] {query}\n")

    results = search(query, k=10)
    if not results:
        print("Nenhum resultado encontrado.")
    else:
        for i, (doc, score) in enumerate(results, 1):
            print(f"--- Resultado {i} (score: {score:.4f}) ---")
            print(doc.page_content[:300])
            print()