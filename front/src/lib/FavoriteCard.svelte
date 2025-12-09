<script>
	let { person, onRemove } = $props();
	let deleting = $state(false);
	let error = $state(""); // Guarda mensagem de erro ao tentar remover
	
	const placeholderImage = "https://placehold.co/500x750/cccccc/333333?text=Sem+Foto";

	// Substitui a imagem caso o link da API esteja vazio ou quebrado
	function handleImageError(e) {
		e.target.src = placeholderImage;
	}

    // Converte o ID do genero para texto
    function formatGender(genderId) {
		if (genderId === 1) return "Feminino";
		if (genderId === 2) return "Masculino";
		return "Não informado";
	}

	// Remove o artista dos favoritos
	async function removeFavorite() {
		if (deleting) return; // Evita clique duplo
		deleting = true;
		error = ""; // Limpa mensagens anteriores

		try {
            if (!person.id) {
                error = "ID invalido nao e possivel remover este favorito";
                deleting = false;
                return;
            }

            const res = await fetch(`http://localhost:8000/favorites/person/${person.id}`, {
                method: "DELETE"
            });

            if (!res.ok) throw new Error("Falha ao remover");

            onRemove?.(); // Atualiza lista de favoritos
        } catch (err) {
            console.error(err);
            error = "Erro ao remover Tente novamente";
            deleting = false;
        }
    }
	// URL da imagem do artista
	const imageUrl = person.profile_url || placeholderImage;
</script>

<div class="person-card" class:deleting_state={deleting}>

	<div class="image-container">
		<img
			src={imageUrl}
			alt={`Foto de ${person.name}`}
			onerror={handleImageError}
			loading="lazy"
		/>
	</div>

	<div class="info-container">
		<h2 class="person-name">{person.name}</h2>

		{#if person.popularity}
			<p class="person-adicionais">
				Popularidade: <span>{person.popularity.toFixed(1)}</span>
			</p>
		{/if}
        {#if person.id}
			<p class="person-adicionais">
				ID: <span>{person.id}</span>
			</p>
		{/if}

		{#if person.gender}
			<p class="person-adicionais">
				Gênero: <span>{formatGender(person.gender)}</span>
			</p>
		{/if}

		{#if error}
			<p class="error-message">{error}</p>
		{/if}

		<!-- Botao para remover artista -->
		<button
			class="remove-btn"
			onclick={removeFavorite}
			disabled={deleting}
		>
			{deleting ? "Removendo..." : "Remover"}
		</button>
	</div>
</div>

<style>
	/* Card do artista com limite de tamanho e sombra */
    .person-card {
        position: relative;
        width: 100%;
        max-width: 240px;
        background: #fff;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        font-family: Arial, sans-serif;
    }

	/* Card fica transparente enquanto remove */
	.person-card.deleting_state {
		opacity: 0.5;
		pointer-events: none;
	}

	/* Container da imagem com proporcao 2:3 */
	.image-container {
		width: 100%;
		aspect-ratio: 2 / 3; 
		background-color: #eee;
	}

	.image-container img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		display: block;
	}

	/* Informacoes do artista */
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

    /* Dados adicionais como genero e popularidade */
    .person-adicionais {
		font-size: 0.85rem;
		color: #666666;
		margin: 0 0 4px 0;
	}

	.person-adicionais span {
		font-weight: bold;
		color: #333;
	}

	/* Mensagem de erro ao remover */
	.error-message {
		font-size: 0.75rem;
		color: #dc2626;
		margin: 0 0 8px 0;
		text-align: center;
		font-weight: bold;
	}

	/* Botao de remover artista */
	.remove-btn {
		margin-top: auto;
		width: 100%;
		padding: 8px 0;
		background-color: #ef4444;
		color: white;
		border: none;
		border-radius: 4px;
		font-size: 0.9rem;
		font-weight: bold;
		cursor: pointer;
		transition: background-color 0.2s ease;
	}

	.remove-btn:hover {
		background-color: #dc2626;
	}

	.remove-btn:disabled {
		background-color: #fca5a5;
		cursor: not-allowed;
	}
</style>
