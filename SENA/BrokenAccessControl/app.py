from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'S3CR3T' 

USERS = {
    "admin": {"password": "adminpassword", "role": "admin"},
    "usuario1": {"password": "userpassword1", "role": "user"},
    "usuario2": {"password": "userpassword2", "role": "user"}
}

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'], role=session['role'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USERS and USERS[username]['password'] == password:
            session['username'] = username
            session['role'] = USERS[username]['role']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', message="Credenciales incorrectas")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'], role=session['role'])

@app.route('/admin_panel')
def admin_panel():

    if 'username' not in session:
        return redirect(url_for('login')) 

    return render_template('admin_panel.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True)
