from flask import Flask, render_template, render_template_string
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/debug")
def debug():
    return os.popen("ls -la").read().replace("\n", "<br>")

@app.route("/.env")
def show_env():
    try:
        with open(".env", "r") as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
