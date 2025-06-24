from flask import Flask, request, redirect, make_response, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        resp = make_response(redirect("/dashboard"))
        resp.set_cookie("role", "user")
        if username == "admin":
            resp.set_cookie("role", "admin") 
        return resp
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    role = request.cookies.get("role")
    if role == "admin":
        return render_template("admin.html")
    return "<h3>Panel de usuario normal</h3><p>No tienes acceso a la sección de admin.</p>"

if __name__ == "__main__":
    app.run(debug=True)
