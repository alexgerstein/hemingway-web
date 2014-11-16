from flask.ext.wtf import Form
from wtforms import SelectField, TextAreaField
from wtforms.validators import ValidationError


class WordLength(object):
    def __init__(self, max=-1, message=None):
        self.max = max
        if not message:
            message = u'Input cannot be more than %i words long.' % (max)
        self.message = message

    def __call__(self, form, field):
        l = field.data and len(field.data.split(" ")) or 0
        if self.max != -1 and l > self.max:
            raise ValidationError(self.message)


class InputForm(Form):
    input_text = TextAreaField('Input', validators=[WordLength(max=300)])
    style = SelectField('Style',
                        choices=[("dickens", "Dickens"), ("shakespeare", "Shakespeare"), ("hemingway", "Hemingway"), ("rappers", "Rappers")])
