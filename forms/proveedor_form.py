from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email

class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre de la Empresa', validators=[DataRequired(message="El nombre es obligatorio.")])
    contacto = StringField('Persona de Contacto', validators=[DataRequired(message="El contacto es obligatorio.")])
    email = EmailField('Correo Electrónico', validators=[DataRequired(message="El correo es obligatorio."), Email()])
    submit = SubmitField('Guardar Proveedor')