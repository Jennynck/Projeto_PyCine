<script>
let { data } = $props();
let quote = data[0];
</script>

<div class="container">
  <div class="quote">{quote.q}</div>
  <div class="author">{quote.a}</div>
  <div class="content">{@html quote.h }</div>
  <pre>{JSON.stringify(data, null, 4)}</pre>
</div>

<style>
.container{
  background-color: #dae9e4;
  padding: 1rem;
  border-radius: 3px;
  border: 1px solid #ccc;
  box-shadow: 0px 2px 0px 0px #ccc;
}
pre{
  background-color: #f5f2f2;
}
.quote{
  font-style: italic;
}
</style>