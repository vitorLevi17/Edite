##formularios
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FileField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired,Email,EqualTo,Length, ValidationError
from edite.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators = [DataRequired(),Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    bt_confirme = SubmitField("Entrar")

class FormCriarConta(FlaskForm):
    nome = StringField("Nome usuario",validators=[DataRequired()])
    email = StringField("E-mail",validators=[DataRequired(),Email()])
    senha = PasswordField("Senha", validators=[DataRequired(),Length(6,20)])
    conf_senha = PasswordField("Senha", validators=[DataRequired(), EqualTo("senha")])
    bt_confirme = SubmitField("Criar conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email = email.data).first()
        if usuario:
            return ValidationError("Email já cadastrado, use outro")


class FormFoto(FlaskForm):
    foto = FileField("foto",validators = [DataRequired()])
    bt_confirme = SubmitField("Enviar foto")


class FormFotoEditar(FlaskForm):
    foto_edi = FileField("foto",validators=[DataRequired()])
    bt_pre_bra = SubmitField("Sem cores")
    bt_sem_fundo = SubmitField("Remover fundo")
    bt_espelhar_imagem = SubmitField("Espelhar imagem")
    bt_comprimir = SubmitField("Comprimir imagem")
    action = HiddenField('')



