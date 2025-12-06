<script>
    import { onMount } from "svelte";
    import FavoriteCard from "./FavoriteCard.svelte";

    // Lista de artistas favoritos
    let favorites = $state([]);
    // Controla se os dados ainda estão carregando
    let loading = $state(true);
    // Armazena mensagens de erro caso algo falhe
    let error = $state("");

    // Busca os artistas favoritos no backend
    async function loadFavorites() {
        loading = true; // Ativa indicador de carregamento
        error = ""; // Limpa mensagens de erro anteriores

        try {
            // Chamada para API que retorna os favoritos
            const res = await fetch("http://localhost:8000/favorites/person");

            // Se a resposta falhar, lança erro
            if (!res.ok) throw new Error("Erro ao carregar favoritos");

            // Atualiza a lista com os dados recebidos
            favorites = await res.json();
        } catch (err) {
            // Salva mensagem de erro para exibir na tela
            error = err.message;
        } finally {
            // Desativa indicador de carregamento
            loading = false;
        }
    }

    // Executa a funcao ao montar o componente
    onMount(() => {
        loadFavorites();
    });

</script>

<!-- Mostra carregamento enquanto os dados estão vindo -->
{#if loading}
    <p>Carregando...</p>
<!-- Mostra erro caso a requisicao falhe -->
{:else if error}
    <p style="color: red">{error}</p>
<!-- Mostra mensagem caso nao haja favoritos -->
{:else if favorites.length === 0}
    <p>Nenhum artista favorito salvo ainda</p>
<!-- Exibe lista de cards de artistas -->
{:else}
    <div class="grid">
        {#each favorites as person}
            <FavoriteCard {person} onRemove={loadFavorites} />
        {/each}
    </div>
{/if}

<style>
    /* Grid responsivo para os cards de artistas */
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 1.2rem;
        padding: 1rem;
    }
</style>
