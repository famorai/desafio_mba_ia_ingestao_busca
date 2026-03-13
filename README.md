# 📚 AI Semantic Search Lab

**RAG com LangChain + Groq + Neon + Ollama Embeddings**

Sistema de **ingestão e busca semântica em documentos** utilizando arquitetura **RAG (Retrieval Augmented Generation)**.

Este laboratório demonstra como construir um pipeline completo de **AI Search** capaz de:

* ingerir documentos
* gerar embeddings
* armazenar vetores
* realizar busca semântica
* gerar respostas baseadas em contexto

A arquitetura foi projetada para funcionar **em ambientes corporativos restritos**, onde há limitações como:

* impossibilidade de uso de Docker
* restrições de download dentro da VPN
* limitação de memória local
* restrições de certificados governamentais

Por isso o projeto utiliza uma **arquitetura híbrida de IA**, combinando serviços remotos com execução local leve.

---

# 🧠 Arquitetura da Solução

A arquitetura segue o padrão **RAG (Retrieval Augmented Generation)**.

Fluxo geral:

1. Documentos PDF são carregados
2. O conteúdo é dividido em *chunks*
3. Cada chunk é convertido em embedding
4. Os embeddings são armazenados no banco vetorial
5. Perguntas do usuário são transformadas em embedding
6. O sistema busca os chunks mais relevantes
7. O contexto recuperado é enviado ao LLM
8. O LLM gera a resposta baseada no contexto

---

# 🏗 Arquitetura Técnica

```mermaid
flowchart TD

A[PDF Documents] --> B[Chunking]
B --> C[Generate Embeddings]

C --> D[Ollama Embedding Model]
D --> E[Vector Storage]

E --> F[Neon PostgreSQL + pgvector]

User[User Question] --> Q[Query Embedding]

Q --> R[Semantic Search]

R --> F

F --> S[Top K Chunks]

S --> LLM[Groq LLM]

LLM --> Answer[Final Answer]
```

---

# 🧩 Componentes da Arquitetura

## LLM (Geração de Respostas - GROQ)

O modelo de linguagem é executado remotamente ( Groq api key ) para reduzir consumo de memória local.

Modelo utilizado:

```
llama-3.1-8b-instant
```

Benefícios:

* baixa latência
* execução remota
* plano gratuito disponível
* integração direta com LangChain

---

## Embeddings

Os embeddings são gerados localmente via **Ollama**.

Modelo utilizado:

```
nomic-embed-text
```

Configuração:

```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3:mini
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

Vantagens:

* execução local
* sem dependência de APIs pagas
* baixo consumo de memória
* bom desempenho para busca semântica

---

## Banco Vetorial

O armazenamento vetorial utiliza **PostgreSQL com extensão pgvector** hospedado no **Neon**.

Benefícios:

* banco serverless
* plano gratuito
* compatibilidade nativa com PostgreSQL
* integração simples com LangChain
* não requer instalação local

---

# 📂 Estrutura do Projeto

```
desafio_mba_ia_ingestao_busca
├── assets
│   └── images
│       ├── evidencia-1-chat.PNG
│       ├── evidencia-2-chat.PNG
│       ├── evidencia-pgvector-postgress.PNG
│       └── evidencia-search.PNG
├── docs
│   └── adr
│       ├── ADR-001-llm-e-embeddings.md
│       └── ADR-002-vector-database.md
│   
│   ├── desafio_doc.pdf
│
├── src
│   ├── chat.py
│   ├── ingestion.py
│   ├── search.py
│
├── .env
├── requirements.txt
└── README.md
```

---

# ⚙️ Instalação 
### Obs: Após executar os procedimentos de clonagem no git. 

## 1️⃣ Criar ambiente virtual

```
python -m venv venv
```

Linux / Mac

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

---

## 2️⃣ Instalar dependências

```
pip install -r requirements.txt
```

Principais bibliotecas:

* langchain
* langchain-community
* langchain-groq
* psycopg
* pgvector
* ollama
* python-dotenv

---

# 🔐 Configuração

Criar arquivo `.env`

```
GROQ_API_KEY=your_api_key

GROQ_MODEL=llama-3.1-8b-instant

PGVECTOR_URL=postgresql://user:password@host/database

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3:mini
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

---

# 🧪 Preparar Ambiente de Embeddings

Instalar Ollama:

```
curl https://ollama.ai/install.sh | sh
```

Baixar modelo de embeddings:

```
ollama pull nomic-embed-text
```

Baixar modelo leve auxiliar:

```
ollama pull phi3:mini
```

---

# 📥 Ingestão de Documentos

Antes de realizar buscas, é necessário **inserir o documento**.

Executar:

```
python src/ingest.py
```

Processo executado:

```
PDF → chunk → embedding → pgvector
```

Fluxo:

```mermaid
flowchart LR

A[PDF] --> B[Chunking]
B --> C[Embedding]
C --> D[pgvector Database]
```

Ao final, os vetores estarão armazenados no banco.

---

# 🔎 Testando Busca Semântica

Para testar a recuperação de contexto:

```
python src/search.py
```

Exemplo de consulta:

```
python src/search.py faturamento
```

O sistema retornará os **chunks mais relevantes**. Isso valida se o chunk correto foi recuperado.

---

# 💬 Executar Chat Semântico

Depois da ingestão, iniciar o chat:

```
python src/chat.py
```

Interface:

```
============================================================
Desafio 1 MBA Engenharia de IA - Ingestão e Busca Semântica
============================================================
Chat PDF — Busca Semântica com LangChain + pgVector
Digite 'sair' para encerrar
============================================================
```

Exemplo:

```
PERGUNTA:
Qual o faturamento da Empresa SuperTechIABrazil?

RESPOSTA:
O faturamento foi de 10 milhões de reais.

PERGUNTA:
"Qual é a capital do Brasil?"

RESPOSTA:
"Não tenho informações necessárias para responder sua pergunta."
```

---

# 🔍 Exemplo de Fluxo de Consulta

```mermaid
sequenceDiagram

participant User
participant App
participant DB
participant LLM

User->>App: Pergunta
App->>App: Gerar embedding
App->>DB: Buscar vetores similares
DB-->>App: Top K chunks
App->>LLM: Contexto + pergunta
LLM-->>App: Resposta
App-->>User: Resposta final
```

---

# 📄 Documentação Arquitetural

O projeto utiliza **ADRs (Architecture Decision Records)** para registrar decisões técnicas.

```
docs/
 └── adr/
     └── ADR-001-groq-llm.md
     └── ADR-002-banco-vetorial
```
# 📸 Evidências de Execução

## Ingestão de documentos
![Ingestão de documentos](./assets/images/evidencia-ingest.PNG)

## Execução da busca semântica
![Execução da busca](./assets/images/evidencia-search.PNG)

## Execução do chat exemplo do desafio

![Execução do chat](./assets/images/evidencia-citada-no-desafio.PNG)

## Execução do chat perguntas e respostas

![Execução do chat](./assets/images/evidencia-1-chat.PNG)

## Execução do chat perguntas e respostas 2

![Execução do chat](./assets/images/evidencia-2-chat.PNG)

## Banco de dados vetorial Neon
![Banco de dados](./assets/images/evidencia-pgvector-postgress.PNG)

---

# 📊 Casos de Uso

Este projeto pode ser utilizado para:

* assistentes internos corporativos
* análise de documentos
* suporte baseado em conhecimento
* busca inteligente em bases documentais
* chatbots baseados em conteúdo

---

# 🚀 Próximos Passos

Possíveis evoluções:

* cache semântico
* reranking de resultados
* observabilidade de pipelines de IA
* ingestão de múltiplos tipos de documento
* API REST para o chat
* interface web

---

# ⭐ Conclusão

Este projeto demonstra como construir um **sistema moderno de busca semântica com RAG**, mesmo em ambientes com restrições corporativas.

A arquitetura híbrida utilizada permite:

* reduzir consumo de recursos locais
* evitar dependência de APIs pagas
* manter pipeline completo de IA
* operar com infraestrutura mínima

# 👨‍💻 Autor

<h4 align="center">
    Feito com 💜 por <a href="https://www.linkedin.com/in/f%C3%A1bio-morais-b34a2729/" target="_blank">Fábio Morais</a>
</h4>
Arquiteto de Sistemas / Engenharia de IA

MBA FullCycle Engenharia de IA - Desafio 1 - 
Projeto desenvolvido como laboratório de **Engenharia de IA aplicado a RAG e busca semântica**.

