<script>
import "../app.css"
let {children} = $props();
</script>

<main>
  <header>
    <h1><a href={`/`}>app</a></h1>
		<nav>
			<a href={`/movies`}>movies</a>
			<a href={`/quotes`}>quotes</a>
      <a href={`/persons`}>persons</a>
      <a href={`/favorites`}>favorites</a>
		</nav>
  </header>

	{@render children?.()}

</main>

<style>
main {
  display: grid;
  grid-template-columns: 1fr;
  padding: 1rem;
	padding-bottom: 2rem;
  background-color: #ebebeb;
}
header{
  display: flex;
  gap: 20px;
  align-items: flex-end;
  border-radius: 3px;
  padding: 10px 10px;
  background-color: rgb(58, 66, 63);
  color: white;
  font-family: "Overpass Mono";
  font-size: small;  
}
h1{
  font-size: medium;
  margin: 0;
  padding: 0;
}
header a, 
header a:visited{
  color: rgb(105, 253, 12);
  text-decoration: none;
}
header a:hover{
	text-decoration: underline;
}
header h1 a, 
header h1 a:visited{
  color: #f5f2f2;
}
header h1 a:hover{
	text-decoration: none;
}
</style>