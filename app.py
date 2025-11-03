from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def fnum(x):
    # Formata bonito: inteiros sem .0, floats curtos
    if x is None:
        return "0"
    if abs(x - int(x)) < 1e-12:
        return str(int(x))
    return f"{x:.4f}".rstrip("0").rstrip(".")

def vec3_from(form_prefix):
    def _val(suf):
        raw = request.form.get(f"{form_prefix}{suf}", "").strip()
        try:
            return float(raw) if raw != "" else 0.0
        except ValueError:
            return 0.0
    return [_val("x"), _val("y"), _val("z")]

def is_zero_vec(v):
    return abs(v[0]) < 1e-12 and abs(v[1]) < 1e-12 and abs(v[2]) < 1e-12

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/operacao", methods=["POST"])
def operacao():
    v1 = vec3_from("v1")
    v2 = vec3_from("v2")
    v3 = vec3_from("v3")
    # escalar é usado em multiplicação e (opcionalmente) para gerar v3 = k*v2 no produto misto
    try:
        k = float(request.form.get("escalar", "0").strip() or 0)
    except ValueError:
        k = 0.0

    op = request.form.get("tipo", "")
    passos = ""
    resultado = None

    # 1) Adição
    if op == "soma":
        res = [v1[i] + v2[i] for i in range(3)]
        passos = (
            f"v₁ + v₂ = (x₁ + x₂, y₁ + y₂, z₁ + z₂)\n"
            f"= ({fnum(v1[0])} + {fnum(v2[0])}, {fnum(v1[1])} + {fnum(v2[1])}, {fnum(v1[2])} + {fnum(v2[2])})\n"
            f"= ({fnum(res[0])}, {fnum(res[1])}, {fnum(res[2])})"
        )
        resultado = res

    # 2) Multiplicação por escalar
    elif op == "multiplicacao_escalar":
        res = [k * c for c in v1]
        passos = (
            f"k·v₁ = k·(x₁, y₁, z₁)\n"
            f"= ({fnum(k)}·{fnum(v1[0])}, {fnum(k)}·{fnum(v1[1])}, {fnum(k)}·{fnum(v1[2])})\n"
            f"= ({fnum(res[0])}, {fnum(res[1])}, {fnum(res[2])})"
        )
        resultado = res

    # 3) Produto escalar
    elif op == "produto_escalar":
        a = v1[0]*v2[0]
        b = v1[1]*v2[1]
        c = v1[2]*v2[2]
        dot = a + b + c
        passos = (
            f"v₁·v₂ = x₁x₂ + y₁y₂ + z₁z₂\n"
            f"= ({fnum(v1[0])}·{fnum(v2[0])}) + ({fnum(v1[1])}·{fnum(v2[1])}) + ({fnum(v1[2])}·{fnum(v2[2])})\n"
            f"= {fnum(a)} + {fnum(b)} + {fnum(c)} = {fnum(dot)}"
        )
        resultado = dot

    # 4) Produto vetorial
    elif op == "produto_vetorial":
        cx = v1[1]*v2[2] - v1[2]*v2[1]
        cy = v1[2]*v2[0] - v1[0]*v2[2]
        cz = v1[0]*v2[1] - v1[1]*v2[0]
        passos = (
            "v₁×v₂ = (y₁z₂ − z₁y₂, z₁x₂ − x₁z₂, x₁y₂ − y₁x₂)\n"
            f"= ({fnum(v1[1])}·{fnum(v2[2])} − {fnum(v1[2])}·{fnum(v2[1])}, "
            f"{fnum(v1[2])}·{fnum(v2[0])} − {fnum(v1[0])}·{fnum(v2[2])}, "
            f"{fnum(v1[0])}·{fnum(v2[1])} − {fnum(v1[1])}·{fnum(v2[0])})\n"
            f"= ({fnum(cx)}, {fnum(cy)}, {fnum(cz)})"
        )
        resultado = [cx, cy, cz]

    # 5) Produto misto: [u,v,w] = u·(v×w)
    elif op == "produto_misto":
        # hipóteses cobertas:
        #  - se a usuária preencher v3 → usa v3
        #  - se v3 estiver zerado e houver k → usa w = k·v2
        #  - senão, w = v3 (que pode ser zero; resultado pode ser 0)
        use_k = is_zero_vec(v3) and abs(k) > 1e-12
        w = [k*c for c in v2] if use_k else v3

        # v × w
        vxw = [
            v2[1]*w[2] - v2[2]*w[1],
            v2[2]*w[0] - v2[0]*w[2],
            v2[0]*w[1] - v2[1]*w[0],
        ]
        # u · (v × w)
        scalar = v1[0]*vxw[0] + v1[1]*vxw[1] + v1[2]*vxw[2]

        if use_k:
            w_desc = f"w = k·v₂ = ({fnum(k)}·{fnum(v2[0])}, {fnum(k)}·{fnum(v2[1])}, {fnum(k)}·{fnum(v2[2])}) = ({fnum(w[0])}, {fnum(w[1])}, {fnum(w[2])})\n"
        else:
            w_desc = f"w = v₃ = ({fnum(w[0])}, {fnum(w[1])}, {fnum(w[2])})\n"

        passos = (
            "[u, v, w] = u·(v×w)\n"
            + w_desc +
            "v×w = (y_v z_w − z_v y_w, z_v x_w − x_v z_w, x_v y_w − y_v x_w)\n"
            f"= ({fnum(v2[1])}·{fnum(w[2])} − {fnum(v2[2])}·{fnum(w[1])}, "
            f"{fnum(v2[2])}·{fnum(w[0])} − {fnum(v2[0])}·{fnum(w[2])}, "
            f"{fnum(v2[0])}·{fnum(w[1])} − {fnum(v2[1])}·{fnum(w[0])})\n"
            f"= ({fnum(vxw[0])}, {fnum(vxw[1])}, {fnum(vxw[2])})\n"
            f"u·(v×w) = ({fnum(v1[0])}, {fnum(v1[1])}, {fnum(v1[2])})·({fnum(vxw[0])}, {fnum(vxw[1])}, {fnum(vxw[2])})\n"
            f"= {fnum(v1[0])}·{fnum(vxw[0])} + {fnum(v1[1])}·{fnum(vxw[1])} + {fnum(v1[2])}·{fnum(vxw[2])}\n"
            f"= {fnum(scalar)}"
        )
        resultado = scalar

    else:
        passos = "Operação inválida."
        resultado = None

    return jsonify(resultado=resultado, passos=passos)

if __name__ == "__main__":
    app.run(debug=True)
