##estruturar as entidades e bases de dados
from edite import database,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def carregarUsuario(id):
    return Usuario.query.get(int(id))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer ,primary_key = True)
    nome = database.Column(database.String , nullable = False)
    email = database.Column(database.String , unique = True)
    senha = database.Column(database.String , nullable = False)
    fotos = database.relationship("Foto", backref="usuario", lazy = True)

class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="pexels-melissa-698907.jpg")
    data = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

