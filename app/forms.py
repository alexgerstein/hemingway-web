from flask.ext.wtf import Form
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


class Form(Form):
	input_text = TextAreaField('Input', validators=[DataRequired()])
	style = SelectField('Style', choices=[("shake", "Shakespeare"), ("hem", "Hemingway")])

