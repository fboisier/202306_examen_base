from flask import flash, redirect, render_template, request, session

from flask_app import app
from flask_app.models.usuarios import Usuario
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  

@app.route('/login')
def registro():

    if 'usuario' in session:
        flash("ya estás LOGEADO!!!! eres " + session['usuario']['email'], "info")
        return redirect("/")

    return render_template("login.html")

@app.route('/procesar_login', methods=["POST"])
def procesar_login():
    print(request.form)

    usuario  = Usuario.get_by_email(request.form['email'])
    if not usuario:
        flash("el correo o la contraseña no es válida", "error")
        return redirect("/login")
    
    resultado = bcrypt.check_password_hash(usuario.password, request.form['password'])

    if resultado:
        session['usuario'] = {
            'id': usuario.id,
            'email': usuario.email
        }
        return redirect("/")

    flash("la contraseña o el correo no es válido", "error")
    return redirect("/login")

@app.route('/procesar_registro', methods=["POST"])
def procesar_registro():
    print(request.form)

    errores = Usuario.validar(request.form)
    if len(errores) > 0:
        for error in errores:
            flash(error, "error")
        return redirect("/login")
    
    if request.form["password"] != request.form["confirmar_password"]:
        flash("las contraseñas no son iguales", "error")
        return redirect("/login")

    data = {
        'email': request.form["email"],
        'password': bcrypt.generate_password_hash(request.form["password"])
    }

    id = Usuario.save(data)

    flash("Usuario registrado correctamente", "success")
    return redirect("/login")



@app.route('/salir')
def salir():
    session.clear()
    return redirect("/login")