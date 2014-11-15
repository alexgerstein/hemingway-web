from flask import render_template, request, jsonify
from app import app
from forms import InputForm
from convert import WriteLike


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
  return render_template('index.html',
							form=InputForm())


@app.route('/translate', methods=['POST'])
def translate():
  form = InputForm(request.form)

  if form.validate():
    writer = WriteLike(request.values.get('style'))
    output_text = writer.style_convert_string(request.values.get('input_text'))

    return jsonify( {'output': output_text} )
  
  return jsonify( {'errors': form.errors})

@app.route('/about')
def about():
  return render_template("about.html")

