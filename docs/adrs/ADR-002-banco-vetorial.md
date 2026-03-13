# ADR-002 — Escolha do Neon como Banco Vetorial

## Status

Aceito

## Contexto

O sistema desenvolvido neste projeto implementa um pipeline de **ingestão e busca semântica em documentos**, baseado na arquitetura de **Retrieval Augmented Generation (RAG)**.

A solução exige um mecanismo de armazenamento capaz de:

* Persistir vetores gerados a partir de embeddings
* Executar consultas de similaridade vetorial
* Integrar-se com o framework de orquestração de IA utilizado no projeto
* Operar em ambiente com restrições de infraestrutura corporativa

Durante a definição da arquitetura, foram identificadas **restrições importantes de infraestrutura e segurança** relacionadas ao ambiente de execução.

### Restrições do ambiente corporativo

O projeto foi desenvolvido em uma máquina corporativa sujeita às seguintes limitações:

1. **Impossibilidade de uso de Docker fora da VPN corporativa**

   A política de segurança da empresa impede a execução de containers Docker em ambientes externos à rede corporativa.

2. **Restrições de download dentro da VPN**

   Quando conectado à VPN corporativa, regras de certificados e políticas de segurança governamentais impedem o download de diversos modelos e dependências externas necessárias para o laboratório.

3. **Limitações de instalação de ferramentas adicionais**

   A instalação de novos runtimes ou serviços que exigem permissões administrativas ou execução em containers torna-se inviável no ambiente de desenvolvimento.

Essas restrições dificultam o uso de diversos bancos vetoriais que normalmente exigem:

* execução via containers
* instalação local de serviços adicionais
* dependências complexas de infraestrutura

Diante desse cenário, foi necessário selecionar uma solução que **não exigisse instalação local**, fosse **acessível externamente** e pudesse ser integrada facilmente ao pipeline de RAG.

---

## Decisão

Foi decidido utilizar o banco de dados **Neon**, que fornece uma instância de **PostgreSQL** gerenciada em nuvem com suporte à extensão **pgvector**.

O Neon permite operar um banco PostgreSQL **serverless**, sem necessidade de instalação local ou uso de containers, mantendo compatibilidade total com ferramentas e bibliotecas utilizadas no ecossistema de IA.

A extensão pgvector adiciona ao PostgreSQL suporte nativo para:

* armazenamento de vetores de alta dimensionalidade
* consultas de similaridade vetorial
* índices vetoriais para otimização de busca

---

## Arquitetura resultante

Com essa decisão, o pipeline de busca semântica passou a operar da seguinte forma:

1. Documentos são carregados e segmentados em chunks
2. Cada chunk é convertido em embedding
3. Os vetores são armazenados em uma base PostgreSQL hospedada no Neon utilizando o tipo `vector`
4. Perguntas do usuário são convertidas em embeddings
5. O banco executa consultas de similaridade vetorial para recuperar os chunks mais relevantes
6. O contexto recuperado é enviado ao modelo de linguagem para geração da resposta

---

## Motivações da escolha

Principais razões para adoção do Neon:

* Eliminação da necessidade de instalação de banco local
* Não dependência de containers Docker
* Execução compatível com restrições do ambiente corporativo
* Disponibilidade de plano gratuito adequado para uso em laboratório
* Compatibilidade nativa com PostgreSQL e pgvector
* Integração simples com frameworks de IA e bibliotecas de acesso a dados

---

## Consequências

### Benefícios

* Simplificação da infraestrutura do projeto
* Possibilidade de execução do laboratório mesmo em ambiente corporativo restrito
* Redução da necessidade de gerenciamento de banco local
* Integração direta com pipelines de RAG baseados em PostgreSQL
* Facilidade de escalabilidade futura caso necessário

### Limitações

* Dependência de conectividade com a internet para acesso ao banco
* Dependência de um serviço externo gerenciado
* Limitações de recursos associadas ao plano gratuito

---

## Alternativas descartadas

### Banco PostgreSQL local

A instalação de PostgreSQL local com pgvector foi considerada, porém descartada devido às restrições de instalação de serviços adicionais no ambiente corporativo.

### Bancos vetoriais dedicados

Ferramentas como:

* Milvus
* Weaviate
* Chroma

foram descartadas devido à dependência de execução em containers ou necessidade de infraestrutura adicional.

### Serviços vetoriais gerenciados

Plataformas como:

* Pinecone

também foram avaliadas, porém não foram adotadas por dependerem de serviços proprietários especializados em vetores, enquanto o Neon permite reutilizar o ecossistema PostgreSQL com pgvector.

---

## Data da decisão

Março de 2026

---

## Autor

Responsável pela decisão arquitetural:
Fábio Morais
Arquiteto de Sistemas / Engenharia de IA
