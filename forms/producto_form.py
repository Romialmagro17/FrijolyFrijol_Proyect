from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Producto', validators=[DataRequired(message="El nombre es obligatorio.")])
    precio = DecimalField('Precio', validators=[DataRequired(message="El precio es obligatorio.")])
    stock = IntegerField('Stock', validators=[DataRequired(message="El stock es obligatorio.")])
    submit = SubmitField('Guardar Producto')