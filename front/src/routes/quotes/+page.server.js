async function save(quote) {
    const endpoint = `http://localhost:8000/quotes/save`;
    const options = {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(quote)
    };
    const res = await fetch(endpoint, options);
    const data = await res.json();
    if (res.ok) {
        console.log(data);
        return data;
    } else {throw new Error(data); }
  }