from flask import render_template
from app import app
from forms import Form

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = Form()

	if form.validate_on_submit():
		return render_template('index.html', 
								input_text=form.input_text.data, 
								output_text=form.input_text.data, 
								form=form)

	return render_template('index.html',
							form=form)