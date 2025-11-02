async function post(url, payload) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function getTriple(prefix) {
  const x = parseFloat(document.getElementById(prefix + "x").value || 0);
  const y = parseFloat(document.getElementById(prefix + "y").value || 0);
  const z = parseFloat(document.getElementById(prefix + "z").value || 0);
  return [x, y, z];
}

function show(elId, value) {
  document.getElementById(elId).textContent = Array.isArray(value)
    ? (${value.map(n => n.toFixed(2)).join(", ")})
    : value;
}

async function sum() {
  try {
    const v1 = getTriple("add-v1");
    const v2 = getTriple("add-v2");
    const data = await post("/api/add", { v1, v2 });
    show("add-out", data.result);
  } catch (e) {
    show("add-out", "Erro: " + e.message);
  }
}

async function scalar() {
  try {
    const v = getTriple("sca-v");
    const k = parseFloat(document.getElementById("sca-k").value || 0);
    const data = await post("/api/scalar", { v, k });
    show("sca-out", data.result);
  } catch (e) {
    show("sca-out", "Erro: " + e.message);
  }
}

async function dot() {
  try {
    const v1 = getTriple("dot-v1");
    const v2 = getTriple("dot-v2");
    const data = await post("/api/dot", { v1, v2 });
    show("dot-out", data.result);
  } catch (e) {
    show("dot-out", "Erro: " + e.message);
  }
}

async function cross() {
  try {
    const v1 = getTriple("cross-v1");
    const v2 = getTriple("cross-v2");
    const data = await post("/api/cross", { v1, v2 });
    show("cross-out", data.result);
  } catch (e) {
    show("cross-out", "Erro: " + e.message);
  }
}
async function plot() {
  try {
    const v1 = getTriple("plot-v1");
    const v2 = getTriple("plot-v2");
    const data = await post("/api/plot", { v1, v2 });
    document.getElementById("plot-img").src = data.image;
    show("plot-out", "Gráfico gerado com sucesso!");
  } catch (e) {
    show("plot-out", "Erro: " + e.message);
  }
}
