from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, RadioField
from wtforms.validators import DataRequired, ValidationError
from setoran_models import check_startend_format


def start_end_validator(form, field):
    if not check_startend_format(field.data):
        raise ValidationError("Wrong value inserted, "
                              "must digit separated by '/'")


class SetoranForm(FlaskForm):
    santri = SelectField(validators=[DataRequired()])
    start = StringField(validators=[DataRequired(), start_end_validator])
    end = StringField(validators=[DataRequired(), start_end_validator])
    jenis = RadioField(validators=[DataRequired()],
                       choices=[("murojaah", "Murojaah"),
                                ("tambah", "Tambah")])
    lulus = RadioField(validators=[DataRequired()],
                       choices=[('1', "Ya"), ('0', "Tidak")])
