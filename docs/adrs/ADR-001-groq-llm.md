# ADR-001 — Escolha de LLM Groq e Embeddings Locais para Sistema de Busca Semântica

## Status

Aceito

## Contexto

O projeto consiste na implementação de um sistema de **ingestão e busca semântica em documentos PDF**, utilizando técnicas de **Retrieval Augmented Generation (RAG)**.

A arquitetura envolve as seguintes etapas:

1. Ingestão de documentos
2. Segmentação em chunks
3. Geração de embeddings
4. Armazenamento vetorial em PostgreSQL com extensão pgvector
5. Recuperação semântica de contexto
6. Geração de resposta utilizando um modelo de linguagem

Durante a definição da arquitetura, algumas **restrições técnicas relevantes** foram identificadas:

### Restrições de infraestrutura

O ambiente de execução possui limitações significativas de recursos:

* Memória RAM limitada
* Ausência de GPU
* Execução local em notebook pessoal
* Impossibilidade de utilização de containers Docker no ambiente do laboratório
* Necessidade de evitar modelos locais de grande porte

Essas restrições inviabilizam o uso de modelos LLM locais maiores, como:

* Llama 3
* Mistral 7B

Esses modelos exigem grande quantidade de memória RAM e frequentemente necessitam de GPU para desempenho adequado.

### Limitações de APIs comerciais

Inicialmente foram avaliadas integrações com provedores de LLM comerciais:

* OpenAI
* Google

Entretanto, as cotas gratuitas disponíveis para:

* GPT-4
* Gemini

foram esgotadas durante os testes iniciais, tornando inviável a continuidade do projeto utilizando essas APIs sem custos adicionais.

### Requisitos do projeto

Além das restrições técnicas, foram considerados os seguintes requisitos:

* Manter o projeto executável em ambiente local
* Minimizar custos operacionais
* Garantir desempenho adequado para consultas
* Permitir integração simples com o framework LangChain
* Suportar arquitetura de busca semântica com banco vetorial

---

## Decisão

Foi decidido utilizar:

### LLM remoto

Modelo hospedado pela empresa Groq.

Modelo selecionado:

* Llama 3.1 8B Instant

Motivações da escolha:

* Disponibilidade de **plano gratuito**
* Baixa latência de inferência
* Integração simples com o ecossistema LangChain
* Execução remota (não consome memória local)

### Embeddings

Para geração de embeddings foi utilizado um modelo local executado através do runtime **Ollama - phi3-mini**.

Modelo escolhido:

* nomic-embed-text

Configuração utilizada:

````
OLLAMA_BASE_URL=http://localhost:11434

OLLAMA_MODEL=phi3:mini
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
````
Motivações:

* Execução totalmente local, eliminando dependência de APIs externas para geração de embeddings
* Baixo consumo de recursos computacionais em comparação com modelos maiores
* Boa qualidade semântica para tarefas de busca vetorial
* Integração simples com pipelines de RAG baseados em LangChain
* Possibilidade de funcionamento offline para a etapa de vetorização

### Estratégia arquitetural adotada

A solução adota uma **arquitetura híbrida de IA**, combinando:

* **LLM remoto** hospedado pela **GROQ** para geração de respostas
* **Embeddings locais** executados Ollama Model, phi3-mini **nomic-embed-text**.

Principais vantagens da estratégia:

* Redução significativa do uso de memória local, já que o modelo de linguagem não precisa ser executado na máquina do usuário
* Eliminação de custos associados a APIs comerciais para geração de embeddings
* Maior controle sobre o processo de vetorização dos documentos
* Arquitetura compatível com padrões modernos de sistemas RAG em produção

---

## Arquitetura resultante

A arquitetura final do sistema ficou estruturada da seguinte forma:

1. Documento PDF é carregado
2. O documento é segmentado em chunks
3. Cada chunk é convertido em embedding
4. Os embeddings são armazenados no banco PostgreSQL utilizando a extensão pgvector
5. Uma pergunta do usuário é convertida em embedding
6. O sistema recupera os chunks mais semanticamente relevantes
7. O contexto recuperado é enviado ao LLM
8. O LLM gera a resposta baseada exclusivamente no contexto fornecido

---

## Consequências

### Benefícios

* Baixo consumo de recursos locais
* Eliminação de dependência de GPU
* Redução de custos operacionais
* Arquitetura compatível com ambientes de produção
* Manutenção de pipeline completo de RAG

### Limitações

* Dependência de acesso à internet para chamadas ao LLM
* Dependência do serviço externo da Groq
* Possíveis limites de requisição do plano gratuito

---

## Alternativas consideradas

### Execução de LLM local

Ferramentas como:

* Ollama

foram avaliadas, porém descartadas devido ao consumo elevado de memória mesmo para modelos compactos.

### Uso de APIs comerciais

APIs avaliadas:

* OpenAI
* Google

Essas alternativas foram descartadas devido à indisponibilidade de cotas gratuitas suficientes para a execução contínua do laboratório.

---

## Data da decisão

Março de 2026

---

## Autor

Responsável pela decisão arquitetural:

Fábio Morais
Arquiteto de Sistemas / Engenharia de IA
