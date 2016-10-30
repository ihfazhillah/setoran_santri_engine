from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SantriForm(FlaskForm):
    nama = StringField(label='Nama', validators=[DataRequired()])
