from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required


# Login form
class LoginForm(Form):
    uname = StringField('Login', validators=[Required()])
    pwd = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Login')

