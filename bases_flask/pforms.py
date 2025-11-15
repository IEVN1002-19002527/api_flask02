from wtforms import Form
from wtforms import StringField, PasswordField, EmailField, BooleanField, IntegerField, SubmitField, RadioField, SelectMultipleField
from wtforms import validators

class UserForm(Form):
    nombre = StringField('Nombre', [validators.DataRequired(message='El campo es requerido')])
    direccion = StringField('Direccion', [validators.DataRequired(message='El campo es requerido')])
    telefono = StringField('Telefono', [validators.DataRequired(message='El campo es requerido')])
    fecha = StringField('Fecha')
    tamano = RadioField('Tamaño', choices=[('chica', 'Chica $40'), ('mediana', 'Mediana $80'), ('grande', 'Grande $120')], validators=[validators.DataRequired()])
    ingredientes = SelectMultipleField('Ingredientes', choices=[('jamon', 'Jamon $10'), ('pina', 'Piña $10'), ('champinones', 'Champiñones $10')])
    npizzas = IntegerField('Num. de Pizzas', [validators.DataRequired(message='El campo es requerido'), validators.NumberRange(min=1)])