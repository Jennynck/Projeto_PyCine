<script>
import { onMount } from "svelte";
import MovieCard from "$lib/MovieCard.svelte";

let results = $state([]);
let genresList = $state([]);
let titleFilter = $state("");
let yearFilter = $state("");
let genreFilter = $state("");
let popularityFilter = $state("");
let errorMessage = $state("");

// Buscar filmes iniciais (top rated)
async function getTopRatedMovies() {
    const res = await fetch("http://localhost:8000/movies/top");
    if (res.ok) {
        results = await res.json();
        errorMessage = "";
    }
}

// Buscar gêneros a partir do endpoint criado no backend para buscar gêneros do TMDB
async function loadGenres() {
    const res = await fetch("http://localhost:8000/genres");
    if (res.ok) {
        genresList = await res.json();
    }
}

// Aplicar filtros
async function applyFilters() {
    const params = new URLSearchParams();
    
    if (titleFilter) params.append("title", titleFilter);
    if (yearFilter) params.append("year", yearFilter);
    if (genreFilter) params.append("genre_id", genreFilter);
    if (popularityFilter) params.append("popularidade_asc_desc", popularityFilter);

    // Se nenhum filtro for aplicado, mantém os top rated
    if (!titleFilter && !yearFilter && !genreFilter && !popularityFilter) {
        return;
    }

    // Busca os filmes no endpoint /discover/movie do tmdb e devolve o json com os dados
    const res = await fetch(`http://localhost:8000/discover/movie?${params}`);
    if (res.ok) {
        const data = await res.json();

        // Caso exista algum erro com os filmes no data irá retornar um erro
        if (data.error) {
            errorMessage = data.error;
            results = [];
            return;
        }

        errorMessage = "";
        results = data;
    }
}

// Limpar filtros
function cleanFilters() {
    titleFilter = "";
    yearFilter = "";
    genreFilter = "";
    popularityFilter = "";
    errorMessage = "";
    getTopRatedMovies();
}

// chama as funções que buscam os filmes top_rated e os gêneros
onMount(() => {
    getTopRatedMovies();
    loadGenres();
});
</script>

<!-- Campos de título, ano e gênero -->
<div class="filters">
    <input type="text" placeholder="Busca por título" bind:value={titleFilter}>
    <input type="number" placeholder="Ano de lançamento" bind:value={yearFilter}>
    
    <select bind:value={genreFilter}>
        <option value="">Todos gêneros</option>
        {#each genresList as g}
            <option value={g.id}>{g.name}</option>
        {/each}
    </select>

    <select bind:value={popularityFilter}>
        <option value="">Popularidade</option>
        <option value="asc">Crescente</option>
        <option value="desc">Decrescente</option>
    </select>

    <!-- botões para acionar as funções de filtragem e limpar filtros -->
    <button onclick={applyFilters}>Filtrar</button>
    <button onclick={cleanFilters}>Limpar</button>
</div>

{#if errorMessage}
    <p class="error">{errorMessage}</p>
{/if}

<div class="results">
    {#if results.length === 0 && !errorMessage}
        <p>Nenhum filme encontrado</p>
    {:else if results.length > 0}
        {#each results as movie}
            <MovieCard item={movie} />
        {/each}
    {/if}
</div>

<style>
.results {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    margin-top: 2rem;
}

.filters {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    align-items: center;
}

.filters input,
.filters select,
.filters button {
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.filters button {
    background: #007bff;
    color: white;
    cursor: pointer;
}
</style>
