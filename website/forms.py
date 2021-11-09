from flask_wtf import FlaskForm
from wtforms import BooleanField, TextField, PasswordField, TextAreaField, StringField, validators, SelectField, SubmitField
from wtforms.validators import Email, DataRequired, Length, ValidationError


class LettersRequired(object):
    def __call__(self, form, field):
        for literka in field.data:
            if literka.isalpha():
                return
        raise ValidationError("Tekst powinien zawierać litery!")


class IsupperRequired(object):
    def __call__(self, form, field):
        for literka in field.data:
            if literka.isupper():
                return
        raise ValidationError("Hasło powinno zawierać wielkie litery!")


class LocalEmail(object):
    def __call__(self, form, field):
        if "@blirt.eu" in field.data:
            return
        raise ValidationError("Podaj firmowy email")


class RegisterForm(FlaskForm):
    login = StringField('Login', [validators.DataRequired(), validators.Length(min=3, max=50)])
    email = StringField("Email", [Email(check_deliverability=True), DataRequired(), LocalEmail()])
    password1 = PasswordField('Password', [validators.DataRequired(), validators.Length(min=7, max=50), validators.EqualTo('password2',message='Passwords must match')])
    password2 = PasswordField('Password confirm', [validators.DataRequired(), validators.Length(min=7, max=50)])


class LoginForm(FlaskForm):
    email = TextField("Adres email", [Email(check_deliverability=True), DataRequired(), LocalEmail()])
    password = TextField("Hasło", [DataRequired()])


class ContactForm(FlaskForm):
    name = TextField("Użytkownik", [validators.DataRequired(), validators.Length(min=3, max=50)])
    email = TextField("Adres email", [Email(check_deliverability=True), DataRequired(), LocalEmail()])
    subject = TextField("Temat wiadomości", [validators.Length(min=3, max=50)])
    message = TextAreaField("Wiadomość", [validators.Length(min=3, max=250)])
    submit = SubmitField("Wyślij")


class ComplainForm(FlaskForm):
    email = StringField("Adres email", [Email(check_deliverability=True), DataRequired(), LocalEmail()])
    complain = TextAreaField("Skarga", [Length(min=10), DataRequired(), LettersRequired()])






