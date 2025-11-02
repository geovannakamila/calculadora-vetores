
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def parse_vec(payload, key):
    # Accepts:
    #  - {"v1":[x,y,z]} style lists, or
    #  - {"v1x":x,"v1y":y,"v1z":z} style fields.
    # Returns a 3-length list of floats.
    if isinstance(payload.get(key), (list, tuple)) and len(payload[key]) == 3:
        try:
            return [float(payload[key][0]), float(payload[key][1]), float(payload[key][2])]
        except Exception:
            raise ValueError(f"Valores de {key} devem ser números.")
    # fallback to v1x/v1y/v1z fields
    try:
        return [
            float(payload.get(f"{key}x", "")),
            float(payload.get(f"{key}y", "")),
            float(payload.get(f"{key}z", "")),
        ]
    except Exception:
        raise ValueError(f"Campos de {key} inválidos. Informe números reais.")


@app.route("/api/add", methods=["POST"])
def api_add():
    data = request.get_json(force=True, silent=False) or {}
    v1 = parse_vec(data, "v1")
    v2 = parse_vec(data, "v2")
    res = [v1[i] + v2[i] for i in range(3)]
    return jsonify(result=res)


@app.route("/api/scalar", methods=["POST"])
def api_scalar():
    data = request.get_json(force=True, silent=False) or {}
    k = float(data.get("k", 0))
    v = parse_vec(data, "v")
    res = [k * x for x in v]
    return jsonify(result=res)


@app.route("/api/dot", methods=["POST"])
def api_dot():
    data = request.get_json(force=True, silent=False) or {}
    v1 = parse_vec(data, "v1")
    v2 = parse_vec(data, "v2")
    res = sum(v1[i] * v2[i] for i in range(3))
    return jsonify(result=res)


@app.route("/api/cross", methods=["POST"])
def api_cross():
    data = request.get_json(force=True, silent=False) or {}
    v1 = parse_vec(data, "v1")
    v2 = parse_vec(data, "v2")
    res = [
        v1[1]*v2[2] - v1[2]*v2[1],
        v1[2]*v2[0] - v1[0]*v2[2],
        v1[0]*v2[1] - v1[1]*v2[0],
    ]
    return jsonify(result=res)


if __name__ == "__main__":
    # For local testing
    app.run(host="0.0.0.0", port=5000, debug=True)
