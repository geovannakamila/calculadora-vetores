from flask import Flask, render_template, request, jsonify, send_file
import matplotlib.pyplot as plt
import io, base64

app = Flask(__name__)

def parse_vec(data, key):
    v = data.get(key)
    if not isinstance(v, list) or len(v) != 3:
        raise ValueError(f"Vetor {key} inválido")
    return [float(x) for x in v]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/add", methods=["POST"])
def api_add():
    data = request.get_json(force=True)
    v1 = parse_vec(data, "v1")
    v2 = parse_vec(data, "v2")
    res = [v1[i] + v2[i] for i in range(3)]
    return jsonify(result=res)

@app.route("/api/scalar", methods=["POST"])
def api_scalar():
    data = request.get_json(force=True)
    v = parse_vec(data, "v")
    k = float(data.get("k", 0))
    res = [k * x for x in v]
    return jsonify(result=res)

@app.route("/api/dot", methods=["POST"])
def api_dot():
    data = request.get_json(force=True)
    v1 = parse_vec(data, "v1")
    v2 = parse_vec(data, "v2")
    res = sum(v1[i] * v2[i] for i in range(3))
    return jsonify(result=res)

@app.route("/api/cross", methods=["POST"])
def api_cross():
    data = request.get_json(force=True)
    v1 = parse_vec(data, "v1")
    v2 = parse_vec(data, "v2")
    res = [
        v1[1]*v2[2] - v1[2]*v2[1],
        v1[2]*v2[0] - v1[0]*v2[2],
        v1[0]*v2[1] - v1[1]*v2[0],
    ]
    return jsonify(result=res)

@app.route("/api/plot", methods=["POST"])
def api_plot():
    data = request.get_json(force=True)
    v1 = parse_vec(data, "v1")
    v2 = parse_vec(data, "v2")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(0, 0, 0, v1[0], v1[1], v1[2], color='purple', label='v1', linewidth=3)
    ax.quiver(0, 0, 0, v2[0], v2[1], v2[2], color='cyan', label='v2', linewidth=3)
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])
    ax.legend()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('Vetores 3D')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return jsonify(image=f"data:image/png;base64,{img_b64}")

if _name_ == "_main_":
    app.run(debug=True)
