<script>
// o componente recebe um parametro
let {item} = $props();
// declara uma variavel "reativa"
let debug = $state(false);

const posterUrl = item.poster_path 
    ? `https://image.tmdb.org/t/p/w500${item.poster_path}`
    : '/placeholder-poster.jpg';
    
</script>

<div>
  <p>{item.title}</p>
  <p>{item.vote_average}</p>
  <p>{item.vote_count}</p>
  <p>{item.release_date}</p>
  <img src={item.poster_url} alt="poster"/>

  <input type="checkbox" bind:checked={debug}/>
  {#if debug}
  <pre>{JSON.stringify(item, null, 2)}</pre>
  {/if}

</div>


<style>
div {
  padding: 1rem;
  border: 1px solid rgb(220, 4, 4);
  width: fit-content;
  max-width: 600px;
}
</style>