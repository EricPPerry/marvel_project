from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo

class SignUpForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    #added extra step to setting password to ensure the user enters the correct password, by entering password2 that must be equal to first password
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    username = StringField('Username', validators=[DataRequired()])

    submit_button = SubmitField()

#new process I research that similar to setting other text fields, can allow the user to change an 'about me section'
class EditProfileForm(FlaskForm):
    about_me = TextAreaField('About me')
    submit = SubmitField()

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit_button = SubmitField()
