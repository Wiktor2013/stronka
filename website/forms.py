from flask_wtf import FlaskForm
from wtforms import BooleanField, TextField, PasswordField, TextAreaField, StringField, validators, SelectField, SubmitField
from wtforms.validators import Email, DataRequired, Length, ValidationError


class LettersRequired(object):
    def __call__(self, form, field):
        for literka in field.data:
            if literka.isalpha():
                return
        raise ValidationError("Text should have letters!")

class IsupperRequired(object):
    def __call__(self, form, field):
        for literka in field.data:
            if literka.isupper():
                return
        raise ValidationError("Text should have letters!")


class ComplainForm(FlaskForm):
    email = StringField("Email", [Email(), DataRequired()])
    complain = TextAreaField("Complain", [Length(min=10), DataRequired(), LettersRequired()])


class ContactForm(FlaskForm):
    name = TextField("Użytkownik")
    email = TextField("Adres email")
    subject = TextField("Temat wiadomości")
    message = TextAreaField("Wiadomość")
    submit = SubmitField("Wyślij")


class RegisterForm(FlaskForm):
    login = StringField('Login', [validators.DataRequired(), validators.Length(min=3, max=50)])
    email = StringField("Email", [Email(), DataRequired()])
    password1 = PasswordField('Password', [validators.DataRequired(), validators.Length(min=7, max=50), validators.EqualTo('password2',message='Passwords must match')])
    password2 = PasswordField('Password confirm', [validators.DataRequired(), validators.Length(min=7, max=50)])
