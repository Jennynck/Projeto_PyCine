<script>
  import { onMount } from "svelte";
  import PersonCard from "$lib/PersonCard.svelte";

  let query = $state("");
  let results = $state([]);
  let errorMessage = $state("");
  let loading = $state(false);

  // variáveis de controle da paginação
  let page = $state(1);
  let totalDisplayed = $state(0);
  let totalResults = $state(0);
  let totalPages = $state(1); 

  // lógica para exibição da lista de números da paginação
  let pageList = $derived.by(() => {
    const gap = 2; 
    let middle = [];
    let finalList = [];

    if (totalPages <= 1) return [1];

    // se tiver poucas páginas, mostra todas de uma vez
    if (totalPages <= 7) {
      for (let i = 1; i <= totalPages; i++) middle.push(i);
      return middle;
    }

    // define o intervalo do meio baseado na página atual
    let start = Math.max(2, page - gap);
    let end = Math.min(totalPages - 1, page + gap);

    for (let i = start; i <= end; i++) {
      middle.push(i);
    }

    // adiciona a primeira página e os pontinhos se precisar
    if (page - gap > 2) finalList.push(1, "...");
    else finalList.push(1);

    // adiciona as páginas do meio na lista
    finalList.push(...middle);

    // coloca a última página e os pontinhos do final
    if (page + gap < totalPages - 1) finalList.push("...", totalPages);
    else if (totalPages > 1) {
       if(finalList[finalList.length - 1] !== totalPages) finalList.push(totalPages);
    }

    return finalList;
  });

  async function getPersons() {
    loading = true;
    errorMessage = "";
    
    // converte para numero para garantir a url certa
    const pageNum = Number(page); 

    let endpoint;
    if (query.trim() === "") {
      // se a busca tiver vazia, pega os populares da página atual
      endpoint = `http://localhost:8000/persons/popular?page=${pageNum}`;
    } else if (!isNaN(query)) {
      // se for número busca pelo id, senão cai no else
      endpoint = `http://localhost:8000/person/${query}`;
    } else {
      // busca artista por nome conforme a página
      endpoint = `http://localhost:8000/person/name/${query}?page=${pageNum}`;
    }

    try {
      const res = await fetch(endpoint);
      const data = await res.json();

      if (!res.ok || data.error) {
        errorMessage = data.error || "Nenhum artista encontrado";
        results = [];
        loading = false;
        return;
      }

      if (query.trim() === "") {

        results = data.results;
        totalDisplayed = results.length;
        totalResults = data.total_results;
        totalPages = data.total_pages > 0 ? data.total_pages : 1; // valida se tem páginas pra não quebrar

      } else {

        let rawResults;

        if (data.results){

          rawResults = data.results;
          totalPages = data.total_pages || 1; // pega o total de páginas que veio da API
          totalResults = data.total_results || rawResults.length;

        } else {
            // busca por id
            rawResults = Array.isArray(data) ? data : [data];
            totalPages = 1; // id é único então só tem 1 página
        }

          results = rawResults;
          totalDisplayed = results.length;
      }

    } catch (err) {
      console.error(err);
      errorMessage = "Erro ao carregar artistas";
      results = [];
    }
    loading = false;
  }
  
  async function handleClick() {
    page = 1;
    await getPersons();
  }

  // reseta a busca e limpa os campos
  async function cleanSearchs() {
    query = "";
    errorMessage = "";
    page = 1;
    await getPersons();
  }

  async function changePage(newPage) {
    // trava cliques repetidos ou inválidos
    if (newPage === "..." || newPage === page) return;
    
    // converte o valor e vê se está dentro do limite de páginas
    const target = Number(newPage);
    if (target < 1 || target > totalPages) return;
    
    // atualiza o estado e faz a busca
    page = target;
    await getPersons();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  onMount(() => {
    getPersons();
  });
</script>

<div class="container">
  <div class="search-box">
    <input 
        placeholder="Digite o nome ou ID do artista" bind:value={query} 
        onkeydown={(e) => e.key === 'Enter' && handleClick()}
    />
    <button class="primary" onclick={handleClick}>Buscar</button>
    <button class="secondary" onclick={cleanSearchs}>Limpar</button>
  </div>

  {#if loading}
    <p>Carregando...</p>
  {:else}
    
    {#if errorMessage}
      <div class="error">{errorMessage}</div>
    {/if}

    {#if !loading && results.length > 0}
      <p class="status-text">
        {#if query}Resultado da busca: {/if}
        Exibindo página <strong>{page}</strong> de <strong>{totalPages}</strong>
      </p>
    {/if}

    <div class="results">
      {#each results as item (item.id)}
        <PersonCard {item} />
      {/each}
    </div>

    {#if totalPages > 1 && results.length > 0} 
      <div class="pagination">
        
        <button 
          type="button" 
          class="nav-btn" 
          onclick={() => changePage(page - 1)} 
          disabled={page === 1}
        >
          Anterior
        </button>

        <div class="page-numbers">
          {#each pageList as p}
            <button 
              type="button" 
              class="page-btn {p === page ? 'active' : ''} {p === '...' ? 'dots' : ''}" 
              onclick={() => changePage(p)} 
              disabled={p === "..."}
            >
              {p}
            </button>
          {/each}
        </div>

        <button 
          type="button" 
          class="nav-btn" 
          onclick={() => changePage(page + 1)} 
          disabled={page === totalPages}
        >
          Próxima
        </button>
      </div>
    {/if}
  {/if}
</div>

<style>
  .container {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding-bottom: 2rem;
  }

  .search-box {
    display: flex;
    gap: 1rem;
    align-items: center;
  }

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

  button {
    cursor: pointer;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    transition: background-color 0.2s, box-shadow 0.2s, transform 0.1s;
    user-select: none;
  }

  .primary {
    padding: 0.75rem 1.25rem;
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

  .secondary {
    padding: 0.75rem 1.25rem;
    background: white;
    color: #96fea4;
    border: 1px solid #3a9d3d;
  }

  .secondary:hover {
    background: #f0f4ff;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .search-box button:last-child {
    background: white;
    color: #0f690f;
    border: 1px solid #115210;
    box-shadow: none;
  }
  
  .search-box button:last-child:hover {
    background: #f0f4ff;
    transform: translateY(-1px);
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

  .status-text {
    color: #666;
    font-size: 0.9rem;
  }

  .pagination {
    margin-top: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .page-numbers {
    display: flex;
    gap: 0.5rem;
  }

  .nav-btn {
    padding: 0.5rem 1rem;
    background-color: #f3f4f6;
    color: #374151;
    border: 1px solid #d1d5db;
    font-size: 0.9rem;
  }

  .nav-btn:hover:not(:disabled) {
    background-color: #e5e7eb;
    border-color: #9ca3af;
  }

  .nav-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .page-btn {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: white;
    border: 1px solid #d1d5db;
    color: #374151;
    border-radius: 8px;
    font-size: 0.95rem;
  }

  .page-btn:hover:not(.active):not(.dots) {
    background-color: #f0fdf4;
    border-color: #20841d;
    color: #09520a;
  }

  .page-btn.active {
    background-color: #09520a;
    color: white;
    border-color: #09520a;
    font-weight: bold;
    transform: scale(1.05);
  }

  .page-btn.dots {
    border: none;
    background: transparent;
    cursor: default;
    color: #9ca3af;
  }

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
    .pagination {
      gap: 0.5rem;
    }
    .page-btn {
      width: 32px;
      height: 32px;
      font-size: 0.8rem;
    }
  }
</style>