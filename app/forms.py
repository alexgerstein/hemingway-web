from flask.ext.wtf import Form
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired


class InputForm(Form):
    input_text = TextAreaField('Input', validators=[DataRequired()])
    style = SelectField('Style',
                        choices=[("dickens", "Dickens"), ("shakespeare", "Shakespeare"), ("hemingway", "Hemingway"), ("rappers", "Rappers")])
