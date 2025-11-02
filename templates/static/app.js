async function post(url, payload) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return res.json();
}

function getVetores() {
  return {
    v1: [
      parseFloat(document.getElementById("v1x").value) || 0,
      parseFloat(document.getElementById("v1y").value) || 0,
      parseFloat(document.getElementById("v1z").value) || 0
    ],
    v2: [
      parseFloat(document.getElementById("v2x").value) || 0,
      parseFloat(document.getElementById("v2y").value) || 0,
      parseFloat(document.getElementById("v2z").value) || 0
    ]
  };
}

async function somar() {
  const res = await post("/api/add", getVetores());
  document.getElementById("resultados").textContent = "Soma: [" + res.join(", ") + "]";
}

async function escalar() {
  const res = await post("/api/dot", getVetores());
  document.getElementById("resultados").textContent = "Produto Escalar: " + res;
}

async function vetorial() {
  const res = await post("/api/cross", getVetores());
  document.getElementById("resultados").textContent = "Produto Vetorial: [" + res.join(", ") + "]";
}

async function gerarGrafico() {
  const res = await post("/api/plot", getVetores());
  document.getElementById("grafico").innerHTML =
    `<img src="data:image/png;base64,${res.image}" alt="Gráfico Vetorial 3D">`;
}
