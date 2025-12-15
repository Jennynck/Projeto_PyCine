<script>
    let { item } = $props();
    let debug = $state(false);

    const tmdbBaseUrl = "https://image.tmdb.org/t/p/w300";
    const placeholderImage = "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png";

    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    let isFavorite = $state(false);

    // --- Funcoes do Backend ---

    async function addFavorite() {
        try {
            const response = await fetch("http://localhost:8000/favorites/person", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(item)
            });
            if (!response.ok) throw new Error("Falha ao salvar favorito");
            return await response.json();
        } catch (error) {
            console.error("Erro ao salvar favorito:", error);
            throw error; 
        }
    }

    // Funcao para salvar favorito
    async function saveFavorite() {
        // Se ja for favorito para aqui, não deixa desmarcar
        if (isFavorite) return; 

        // Se passou, define como true e salva
        const previousState = isFavorite;
        isFavorite = true; 

        try {

            await addFavorite();
            dispatch("favorite", { ...item, isFavorite: isFavorite });

        } catch (error) {

            console.error("Falha ao sincronizar, revertendo.");
            isFavorite = previousState;
        }
    }
</script>

<div class="person-card">
    <button class="favorite-btn" onclick={saveFavorite} aria-label="Salvar artista">
        <svg
            class="heart-icon"
            viewBox="0 0 24 24"
            fill={isFavorite ? "red" : "none"}
            stroke="red"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
        >
            <path
                d="M20.8 4.6c-1.5-1.6-4-1.6-5.5 0L12 7.9l-3.3-3.3c-1.5-1.6-4-1.6-5.5 0s-1.5 4.2 0 5.8L12 21l8.8-10.6c1.6-1.6 1.6-4.2 0-5.8z"
            />
        </svg>
    </button>

    <div class="image-container">
        {#if item.profile_path}
            <img
                src={tmdbBaseUrl + item.profile_path}
                alt={`Foto de ${item.name}`}
                loading="lazy"
            />
        {:else}
            <img
                src={placeholderImage}
                alt="Sem foto"
                class="placeholder"
            />
        {/if}
    </div>

    <div class="info-container">
        <h2 class="person-name">{item.name}</h2>
        <p class="person-popularity">
            Popularidade: <span>{item.popularity ? item.popularity.toFixed(1) : "-"}</span>
        </p>
    </div>

    <div class="debug-save">
        <label>
            <input type="checkbox" bind:checked={debug} />
            Ver JSON
        </label>
    </div>

    {#if debug}
        <pre class="debug-pre">{JSON.stringify(item, null, 2)}</pre>
    {/if}
</div>

<style>
    .person-card {
        position: relative;
        width: 250px;
        background: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        font-family: Arial, sans-serif;
    }

    .image-container {
        width: 100%;
        aspect-ratio: 2 / 3;
        background-color: #e4e4e4;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .image-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }

    .image-container img.placeholder {
        width: 50%;
        height: 50%;
        object-fit: contain;
        opacity: 0.5;
    }

    .info-container {
        padding: 12px;
    }

    .person-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin: 0 0 4px 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .person-popularity {
        font-size: 0.85rem;
        color: #666666;
        margin: 0;
    }
    .person-popularity span {
        font-weight: bold;
    }

    /* --- Estilos do Botao Favorito --- */
    .favorite-btn {
        position: absolute;
        bottom: 10px; 
        right: 10px;  
        background: rgba(255, 255, 255, 0.9);
        border: none;
        cursor: pointer;
        border-radius: 50%;
        padding: 0.35rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
        transition:
            transform 0.15s ease-in-out,
            background 0.2s ease-in-out;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .favorite-btn:hover {
        transform: scale(1.15);
        background: #fff5f5;
    }

    .heart-icon {
        width: 24px;
        height: 24px;
    }
    
    /* --- Estilos do Debug --- */
    .debug-save {
        font-size: 0.8rem;
        padding: 0 12px 12px 12px;
        color: #777;
    }
    .debug-pre {
        background-color: #ffffff;
        color: rgb(0, 0, 0);
        font-size: 0.75rem;
        padding: 10px;
        margin: 0 12px 12px 12px;
        border-radius: 4px;
        overflow-x: auto;
    }
</style>