from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, TelField, SelectField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Optional

listOfState = ["", "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River", "Delta", "Ebonyi", "Edo",  "Ekiti", "Enugu", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun",  "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara", "Abuja"]

class AddPayerForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=1, max=120)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=4, max=120)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=4, max=120)])
    state = SelectField('State', validators=[DataRequired()], validate_choice=True, choices=listOfState)
    phoneNumber = TelField('Phone Number', validators=[Optional(), Length(min=11, max=14)])
    submit = SubmitField('Submit')

class RegisterAccountantForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=120)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', 'Password Must Match!')])
    email = EmailField('Email', validators=[DataRequired(), Length(min=1, max=120)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=4, max=120)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=4, max=120)])
    phoneNumber = TelField('Phone Number', validators=[Optional(), Length(min=11, max=14)])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=120)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Submit')