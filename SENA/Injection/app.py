from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()

        if result:
            message = "✅ Login exitoso: Bienvenido admin"
        else:
            message = "❌ Login fallido"

    return render_template_string('''
        <h2>Login inseguro (SQLi)</h2>
        <form method="POST">
            <input name="username" placeholder="Usuario"><br>
            <input name="password" placeholder="Contraseña"><br>
            <input type="submit" value="Login">
        </form>
        <p>{{ message }}</p>
        ''', message=message)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
