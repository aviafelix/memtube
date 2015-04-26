from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


# Login form
class LoginForm(Form):
    uname = StringField('Login', validators=[DataRequired()])
    pwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

