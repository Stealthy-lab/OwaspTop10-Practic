from flask import Flask, request, render_template_string

app = Flask(__name__)

PRODUCT = {
    "name": "Premium Laptop",
    "price": 1500
}

@app.route("/", methods=["GET"])
def index():
    return render_template_string('''
        <h2>Comprar producto</h2>
        <form method="POST" action="/buy">
            Producto: {{ name }}<br>
            Precio (editable): <input name="price" value="{{ price }}"><br>
            <input type="submit" value="Comprar">
        </form>
    ''', name=PRODUCT["name"], price=PRODUCT["price"])

@app.route("/buy", methods=["POST"])
def buy():
    price = float(request.form["price"])
    if price < 100:
        return "⚠️ ¡El precio es sospechosamente bajo! ¿Intentas hackear?"
    
    return f"✅ Compra completada por ${price:.2f}"

if __name__ == "__main__":
    app.run(debug=True)
