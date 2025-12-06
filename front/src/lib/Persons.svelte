<script>
  import { onMount } from "svelte";
  import PersonCard from "$lib/PersonCard.svelte";

  let query = $state("");        // campo de busca (nome ou id)
  let results = $state([]); 
  let errorMessage = $state("");
  let loading = $state(false);

  // Função para buscar artistas
  async function getPersons() {
    loading = true; 
    errorMessage = "";
    let endpoint;

    // Sem busca = carrega trending da semana
    if (query.trim() === "") {
      endpoint = `http://localhost:8000/persons/trending/week`;
    }
    // Busca por ID 
    else if (!isNaN(query)) {
      endpoint = `http://localhost:8000/person/${query}`;
    }
    // Busca por nome
    else {
      endpoint = `http://localhost:8000/person/name/${query}`;
    }

    try {
      const res = await fetch(endpoint);
      const data = await res.json();

      if (!res.ok || data.error) {
        errorMessage = data.error || "Nenhum artista encontrado";
        results = [];
        return;
      }

      // Sempre garante um array para o #each, caso não receba um array, transforma os dados em um array de uma posição
      let rawResults = Array.isArray(data) ? data : [data];

      // Implementação da validação: Filtra para manter apenas os artistas que possuem 'profile_path' (foto)
      results = rawResults.filter(person => person.profile_path);
      
      // Se após o filtro, o array estiver vazio, exibe uma mensagem específica
      if (results.length === 0) {
        errorMessage = "Nenhum artista encontrado com foto.";
      }

    } catch (err) {
      errorMessage = "Erro ao buscar artistas";
      results = [];
    }
    loading = false; 
  }

  async function saveFavorite(person) {
  try {
    const res = await fetch("http://localhost:8000/favorites/person", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(person)
    });

    if (!res.ok) {
      console.error("Erro ao salvar favorito");
    }
  } catch (err) {
    console.error("Erro ao conectar ao backend", err);
    }
  }

  function handleClick() {
    getPersons();
  }

  async function cleanSearchs(){
    query = "";
    errorMessage = "";
    await getPersons();
  }

  onMount(() => {
    getPersons(); // trending ao abrir página
  });
</script>

<style>
  /* Container */
  .container {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .search-box {
    display: flex;
    gap: 1rem;
    align-items: center;
  }

  /* Input */
  input {
    padding: 0.75rem 1rem;
    font-size: 1rem;
    width: 280px;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    transition: border-color 0.2s, box-shadow 0.2s;
    outline: none;
  }
  
  input:focus {
    border-color: #5c7cfa;
    box-shadow: 0 0 0 3px rgba(92, 124, 250, 0.2);
  }

  /* Botões gerais */
  button {
    padding: 0.75rem 1.25rem;
    cursor: pointer;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    transition: background-color 0.2s, box-shadow 0.2s, transform 0.1s;
    user-select: none;
  }

  /* Botão BUSCAR */
.primary {
  background: #09520a;
  color: white;
  border: 1px solid #115210;
  box-shadow: 0 6px 10px -2px rgba(92, 250, 145, 0.277), 
              0 4px 6px -4px rgba(0, 0, 0, 0.1);
}

.primary:hover {
  background: #20841d;
  transform: translateY(-3px);
  box-shadow: 0 10px 15px -3px rgba(92, 250, 110, 0.55), 
              0 4px 6px -2px rgba(0, 0, 0, 0.15);
}

.primary:active {
  transform: translateY(0) scale(0.98);
}

/* Botão LIMPAR */
.secondary {
  background: white;
  color: #96fea4;
  border: 1px solid #3a9d3d;
}

.secondary:hover {
  background: #f0f4ff;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

  
  /* Botão LIMPAR (Ação Secundária) - ESTILO OUTLINE COM DESTAQUE */
  .search-box button:last-child {
    background: white; /* Fundo branco */
    color: #0f690f; /* Texto azul para contraste */
    border: 1px solid #115210; /* Borda azul */
    box-shadow: none;
  }
  
  .search-box button:last-child:hover {
    background: #f0f4ff; /* Fundo muito leve ao passar o mouse */
    transform: translateY(-1px);
    /* Sombra leve para destacar a interatividade */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); 
  }
  
  .search-box button:last-child:active {
    transform: translateY(0);
  }

  .results {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
  }

  .error {
    color: #ef4444;
    font-size: 1.1rem;
    background-color: #fef2f2;
    padding: 0.75rem;
    border-radius: 6px;
    border: 1px solid #fecaca;
    font-weight: 500;
  }

  /* Responsividade */
  @media (max-width: 600px) {
    .search-box {
      flex-direction: column;
      gap: 0.75rem;
    }
    input {
      width: 100%;
    }
    .search-box button {
      width: 100%;
    }
  }
</style>

<div class="container">
  <div class="search-box">
    <input placeholder="Digite o nome ou ID do artista" bind:value={query} />

    <button class="primary" onclick={handleClick}>Buscar</button>
    <button class="secondary" onclick={cleanSearchs}>Limpar</button>

  </div>

    {#if loading}
      <p>Carregando...</p>
    {:else}
      
      {#if errorMessage}
        <div class="error">{errorMessage}</div>
      {/if}

      <div class="results">
        {#each results as item}
          <PersonCard {item} />
        {/each}
      </div>

    {/if}
</div>

