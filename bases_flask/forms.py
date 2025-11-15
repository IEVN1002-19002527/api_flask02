from wtforms import Form
from wtforms import StringField, PasswordField, EmailField, BooleanField, IntegerField, SubmitField
from wtforms import validators

class UserForm(Form):
    matricula = StringField('Matricula', [validators.DataRequired(message='El campo es requerido')])
    nombre = StringField('Nombre', [validators.DataRequired(message='El campo es requerido')])
    apellido = StringField('Apellido', [validators.DataRequired(message='El campo es requerido')])
    correo = EmailField('Correo', [validators.Email(message='Ingrese correo valido')])