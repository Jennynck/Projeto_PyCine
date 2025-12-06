# PyCine - Integração TMDB & Catálogo de Filmes

> **Status:** Em desenvolvimento

Este projeto é uma aplicação **Full Stack** que integra dados da API pública do **The Movie Database (TMDB)** com um sistema próprio de persistência para gerenciamento de usuários e favoritos.

O objetivo principal é demonstrar a construção de uma **API RESTful robusta com Python**, aplicando arquitetura em camadas, validação de dados estrita e operações assíncronas de banco de dados.

---

## Tecnologias Utilizadas

### Backend (Foco do Projeto)
- **Linguagem:** Python 3.10+
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Alta performance e Async)
- **Banco de Dados:** MongoDB (Atlas)
- **Driver:** Motor (AsyncIO)
- **Validação:** Pydantic V2 (Tipagem estrita & Computed Fields)
- **Integração:** Requests (Consumo de API Externa)

### Frontend
- **Framework:** Svelte/SvelteKit
- **Estilização:** CSS customizado

---

## Destaques Técnicos e Arquitetura

Este projeto foi estruturado pensando em escalabilidade e boas práticas de desenvolvimento Python:

1.  **Padrão Service (Camada de Serviço):**
    - A lógica de negócios e as chamadas externas (TMDB) estão isoladas em classes de serviço (`MovieService`, `PersonService`), mantendo as rotas (`endpoints`) limpas e organizadas.

2.  **Programação Assíncrona (Async/Await):**
    - Uso do driver assíncrono (**Motor**) para todas as operações de banco de dados (MongoDB), garantindo alta performance em operações de I/O.

3.  **Modelagem de Dados Avançada (Pydantic):**
    - Uso de `@computed_field` para gerar URLs de imagens dinamicamente.
    - Validação rigorosa de tipos na entrada e saída da API.

---

## Como Rodar o Projeto Localmente

### Pré-requisitos
- **Backend:** Python 3.10+ e MongoDB.
- **Frontend:** Node.js (v16+) e NPM.

### 1. Configurando o Backend (API)

1. Entre na pasta raiz e crie/ative o ambiente virtual:
   ```bash
   python -m venv env
   # Windows: env\Scripts\activate
   # Linux/Mac: source env/bin/activate


2. Instale as dependências a seguir:
    ```bash
    pip install fastapi uvicorn requests python-dotenv motor pydantic


3. Crie o arquivo .env na raiz (baseado no .env.example) e adicione suas chaves

    ```Ini, TOML

    Arquivo .env.example:

    # Chave da API do TMDB (Obter em: https://www.themoviedb.org/settings/api)
    TMDB_TOKEN=sua_chave_aqui

    # String de conexão do MongoDB Atlas
    MONGODB_URL=mongodb+srv://usuario:senha@cluster.mongodb.net/nome_do_banco

4. Inicie o servidor:

    ```bash
    uvicorn main:app --reload

---   

### 2. Configurando o Frontend (Interface Visual)

1. Abra um **novo terminal** e entre na pasta do projeto visual:
   ```bash
   cd front
2. Instale as dependências do Node.js:
   ```bash
   npm i
3. Inicie o servidor de desenvolvimento:
    ```bash
    npm run dev

O projeto geralmente ficará disponível em: http://localhost:5173
---

Desenvolvido por Jhennifer Nicole
