from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def ssrf_lab():
    result = ""
    if request.method == "POST":
        url = request.form.get("url")
        try:
            if url.startswith("file://"):
                path = url.replace("file://", "")
                with open(path, "r") as f:
                    result = f"<pre>{f.read(1000)}</pre>"
            else:
                response = requests.get(url, timeout=3)
                result = f"<pre>{response.text[:1000]}</pre>"
        except Exception as e:
            result = f"<p style='color:red;'>Error: {e}</p>"

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SSRF Demo - Visor de URLs</title>
    </head>
    <body style="font-family: Arial; text-align: center; margin-top: 60px;">
        <h2>Visor de contenido desde una URL (potencialmente peligrosa)</h2>
        <form method="POST">
            <input type="text" name="url" size="60" placeholder="http://example.com o file:///etc/passwd" />
            <br><br>
            <button type="submit">Cargar Contenido</button>
        </form>
        <hr>
        <div>{{ result|safe }}</div>
    </body>
    </html>
    """, result=result)

if __name__ == "__main__":
    app.run(debug=True)

