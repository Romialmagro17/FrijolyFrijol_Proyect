from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired

class FacturacionForm(FlaskForm):
    numero_factura = StringField('Número de Factura', validators=[DataRequired(message="El número de factura es obligatorio.")])
    cliente = StringField('Cliente', validators=[DataRequired(message="El nombre del cliente es obligatorio.")])
    monto_total = DecimalField('Monto Total', validators=[DataRequired(message="El monto es obligatorio.")])
    fecha = DateField('Fecha', validators=[DataRequired(message="La fecha es obligatoria.")])
    submit = SubmitField('Generar Factura')