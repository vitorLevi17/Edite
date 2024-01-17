##rotas/links do site

from flask import Flask, render_template,redirect ,url_for
from edite import app,database,bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from edite.forms import FormLogin, FormCriarConta,FormFoto
from edite.models import Usuario,Foto
import os
from werkzeug.utils import secure_filename

@app.route("/", methods=["GET", "POST"])
def paginaInicial():
    formLogin = FormLogin()
    if formLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formLogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))


    return render_template("paginaInicial.html", form=formLogin)


@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    formCriarConta = FormCriarConta()
    if formCriarConta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formCriarConta.senha.data)
        usuario = Usuario(nome = formCriarConta.nome.data, email = formCriarConta.email.data, senha = senha)

        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario = usuario.id))
    return render_template("criarconta.html", form=formCriarConta)


@app.route("/perfil/<id_usuario>", methods=["GET" , "POST"])
@login_required
def perfil(id_usuario):
    ##USUARIO = USUARIO

    if int(id_usuario) == int(current_user.id):
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.dirname(__file__), app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            foto = Foto(imagem = nome_seguro, id_usuario =current_user.id)
            database.session.add(foto)
            database.session.commit()

        return render_template("perfil.html", usuario = current_user,form = form_foto)

    else:
        ##USUARIO /= USUARIO

        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario  = usuario, form = None)

@app.route("/logout")
@login_required
def logout():
    login_user(current_user) ##possivel erro
    return redirect(url_for("paginaInicial"))

@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data.desc()).all()
    return render_template("feed.html", fotos=fotos)



