import os

from search import get_context

from langchain_groq import ChatGroq
# from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
# ─── Configuração ────────────────────────────────────────────────────────────

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL   = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# Ollama config
# OLLAMA_LLM   = os.getenv("OLLAMA_MODEL")
# OLLAMA_BASE  = os.getenv("OLLAMA_BASE_URL")

# ─── Prompt Template ─────────────────────────────────────────────────────────

PROMPT_TEMPLATE = """
Você é um assistente que responde perguntas somente com base no CONTEXTO.

CONTEXTO:
{context}

REGRAS:
- Responda EXCLUSIVAMENTE com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda: "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS DENTRO DO CONTEXTO:
PERGUNTA: "Qual o faturamento da Empresa SuperTechIABrazil?"
RESPOSTA: "O faturamento foi de 10 milhões de reais."

PERGUNTA: "Qual o faturamento no ano de fundação 1931?"
RESPOSTA: "O faturamento foi de 85.675.568,77 milhões de reais."

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO: {question}

RESPONDA A "PERGUNTA DO USUÁRIO":"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=PROMPT_TEMPLATE,
)

# ─── LLM ─────────────────────────────────────────────────────────────────────

def get_llm() -> ChatGroq:
    return ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0
        # num_ctx=2048,
    )


# ─── Pipeline de resposta ─────────────────────────────────────────────────────

def answer(question: str) -> str:
    """
    Fluxo completo:
      1. Vetoriza a pergunta.
      2. Busca os 10 chunks mais relevantes.
      3. Monta o prompt.
      4. Chama a LLM.
      5. Retorna a resposta.
    """
    # 1 & 2 — Buscar contexto
    context = get_context(question, k=10)

    if not context:
        return "Não tenho informações necessárias para responder sua pergunta."
    
    # print("\n[DEBUG CONTEXT]")
    # print(context[:500])

    # 3 — Montar prompt
    filled_prompt = prompt.format(context=context, question=question)

    # 4 — Chamar LLM
    llm = get_llm()
    response = llm.invoke(filled_prompt)

    return response.content.strip()


# ─── Loop CLI ─────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 60)
    print("  Desafio 1 MBA Engenharia de IA - Ingestão e Busca Semântica")
    print("  Chat PDF — Busca Semântica com LangChain + pgVector")
    print("  Digite 'sair' ou pressione Ctrl+C para encerrar.")
    print("=" * 60)

    while True:
        try:
            print()
            question = input("PERGUNTA: ").strip()

            if not question:
                continue

            if question.lower() in {"sair", "exit", "quit"}:
                print("Encerrando. Até logo!")
                break

            print("\nRESPOSTA: ", end="", flush=True)
            resposta = answer(question)
            print(resposta)
            print("\n" + "-" * 60)

        except KeyboardInterrupt:
            print("\n\nEncerrando. Até logo!")
            break
        except Exception as e:
            print(f"\n[ERRO] {e}")


if __name__ == "__main__":
    main()