<script>
let { data } = $props();
import Quote from "$lib/Quote.svelte";
async function get_quote(){
  return data.zenquote;
}
</script>

<div>
  <h2>Zenquote API</h2>

  {#await get_quote() then quote }
    <Quote data={quote}></Quote>    
  {/await}

</div>
