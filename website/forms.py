from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, TextAreaField, StringField, validators, SubmitField
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
    first_name = StringField('Imię', [validators.DataRequired(), validators.Length(min=3, max=50)])
    second_name = StringField('Nazwisko', [validators.DataRequired(), validators.Length(min=3, max=50)])
    email = StringField("Email", [Email(check_deliverability=True), DataRequired()])
    password1 = PasswordField('Hasło', [validators.DataRequired(), validators.Length(min=7, max=50),
                                        validators.EqualTo('password2', message='Hasła muszą być takie same')])
    password2 = PasswordField('Potwierdź hasło', [validators.DataRequired(), validators.Length(min=7, max=50)])
    submit = SubmitField("Zarejestruj")


class LoginForm(FlaskForm):
    email = StringField("Adres email", [Email(check_deliverability=True), DataRequired()])
    password = PasswordField("Hasło", [DataRequired()])
    submit = SubmitField("Zaloguj")


class ContactForm(FlaskForm):
    first_name = StringField("Imię", [validators.DataRequired(), validators.Length(min=3, max=50)])
    email = StringField("Adres email", [Email(check_deliverability=True), DataRequired(), LocalEmail()])
    subject = StringField("Temat wiadomości", [validators.Length(min=3, max=50)])
    message = TextAreaField("Wiadomość", [validators.Length(min=3, max=250)])
    submit = SubmitField("Wyślij")


class ComplaintForm(FlaskForm):
    email = StringField("Adres email", [Email(check_deliverability=True), DataRequired(), LocalEmail()])
    complaint = TextAreaField("Skarga", [Length(min=10), DataRequired(), LettersRequired()])


class ForgotForm(FlaskForm):
    email = StringField("Adres email", [Email(check_deliverability=True), DataRequired()])
    submit = SubmitField("Wyślij link")


class ResetForm(FlaskForm):
    password_new = PasswordField('Hasło', [validators.DataRequired(), validators.Length(min=7, max=50),
                                           validators.EqualTo('password_new_conf', message='Hasła muszą być takie same')])
    password_new_conf = PasswordField('Potwierdź hasło', [validators.DataRequired(), validators.Length(min=7, max=50)])
    submit = SubmitField("Zresetuj hasło")
