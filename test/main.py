from flask import Flask, render_template, request
from wtforms import Form, SelectField, StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class MyForm(Form):
    choice = SelectField('Choose an option', choices=[('1', 'Option 1'), ('2', 'Option 2')], default='1')
    name = StringField('Your Name', validators=[DataRequired()])
    
    # Additional fields for option 2
    home = StringField('Home', validators=[DataRequired()])
    id = StringField('ID', validators=[DataRequired()])
    num = StringField('Number', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm(request.form)
    
    # This is to check if the form is submitted and valid
    if form.validate_on_submit():
        if form.choice.data == '1':
            user_info = f"User's Name: {form.name.data}"
        else:
            user_info = f"User's Info: {form.name.data}, {form.home.data}, {form.id.data}, {form.num.data}"
        return render_template('result.html', user_info=user_info)

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

