from flask import render_template
from app import app
from forms import Form
from convert import WriteLike

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = Form()

	if form.validate_on_submit():
		writer = WriteLike(form.style.data)

		output_text = writer.style_convert_string(form.input_text.data)

		return render_template('index.html', 
								input_text=form.input_text.data, 
								output_text=output_text, 
								form=form)

	return render_template('index.html',
							form=form)

@app.route('/about')
def about():
	return render_template("about.html")
