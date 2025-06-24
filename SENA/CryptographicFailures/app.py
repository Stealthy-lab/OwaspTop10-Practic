from flask import Flask, render_template, request, redirect, url_for, session
import hashlib

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura_para_el_lab_de_flask' # Clave secreta para las sesiones

# *** VULNERABILIDAD: ALMACENAMIENTO DE CONTRASEÑAS INSEGURO (MD5 sin salt) ***
# Estas son las contraseñas pre-hasheadas en MD5. Cuando el usuario ingrese
# la contraseña en texto plano, la aplicación la hasheará y la comparará con estos valores.
#
# Credenciales de prueba (contraseña en texto plano -> su hash MD5):
# "admin123"       -> "21232f297a57a5a743894a0e4a801fc3"
# "passwordsegura" -> "37604f32a76f28682a0b8180376241a7"
USER_PASSWORDS_VULNERABLE = {
    "admin": "21232f297a57a5a743894a0e4a801fc3",
    "usuario": "37604f32a76f28682a0b8180376241a7",
}

@app.route('/')
def index_crypto():
    if 'username' in session:
        return render_template('index_crypto.html', username=session['username'])
    return redirect(url_for('login_crypto'))

@app.route('/login', methods=['GET', 'POST'])
def login_crypto():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hashear la contraseña ingresada por el usuario usando MD5
        hashed_password_input = hashlib.md5(password.encode('utf-8')).hexdigest()

        # DEBUG: Imprime los hashes para ver qué está sucediendo
        print(f"DEBUG - Usuario ingresado: {username}")
        print(f"DEBUG - Contraseña ingresada (hasheada): {hashed_password_input}")
        if username in USER_PASSWORDS_VULNERABLE:
            print(f"DEBUG - Hash almacenado para {username}: {USER_PASSWORDS_VULNERABLE[username]}")
        else:
            print(f"DEBUG - Usuario {username} NO encontrado en la base de datos simulada.")

        # Comparar el hash de la contraseña ingresada con el hash MD5 almacenado
        if username in USER_PASSWORDS_VULNERABLE and \
           USER_PASSWORDS_VULNERABLE[username] == hashed_password_input:
            session['username'] = username
            return redirect(url_for('dashboard_crypto'))
        else:
            return render_template('login_crypto.html', message="Credenciales incorrectas")
    return render_template('login_crypto.html')

@app.route('/dashboard')
def dashboard_crypto():
    if 'username' not in session:
        return redirect(url_for('login_crypto'))
    return render_template('dashboard_crypto.html', username=session['username'])

@app.route('/logout')
def logout_crypto():
    session.pop('username', None)
    return redirect(url_for('login_crypto'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
