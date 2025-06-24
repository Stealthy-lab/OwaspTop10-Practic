from flask import Flask, request, render_template_string, send_from_directory
import os

app = Flask(__name__)
os.makedirs("logs", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Guardar intento en el log
        with open("logs/access.log", "a") as log:
            log.write(f"Usuario: {username} - Contraseña: {password}\n")

        if username == "admin" and password == "1234":
            message = "✅ FLAG: CTF{log_exposed_login_success}"
        else:
            message = "❌ Usuario o contraseña incorrecta."

    return render_template_string("""
        <html>
        <body style="text-align:center; margin-top:100px;">
            <h2>Login inseguro</h2>
            <form method="POST">
                <input name="username" placeholder="Usuario"><br><br>
                <input name="password" type="password" placeholder="Contraseña"><br><br>
                <button>Ingresar</button>
            </form>
            <p>{{ message }}</p>
            <p style="font-size:12px;">¿Eres admin? <a href="/logs/access.log">Ver logs</a></p>
        </body>
        </html>
    """, message=message)

@app.route("/logs/<path:filename>")
def get_log(filename):
    return send_from_directory("logs", filename)

if __name__ == "__main__":
    app.run(debug=True)
