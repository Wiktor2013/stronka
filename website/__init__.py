from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, TextAreaField, SubmitField
from datetime import datetime
from string import punctuation
from flask_sqlalchemy import SQLAlchemy #0. Instalacja i import SQLAlchemy (requirements.txt)
import re
from flask_migrate import Migrate

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

app = Flask(__name__)
app.secret_key = 'dupa'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" #1 Dodanie info o rodzaju bazy i gdzie jest
db = SQLAlchemy(app=app) #2. Dodanie obiektu

#3. stworzenie modelu/tabeli
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    email = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(25))

#4. stworzenie obiektu migracji
migrate = Migrate(app=app, db=db)

#5. Wykonanie migracji w terminalu
#Migracja - to skrypt ktory tworzy/modyfikuje strukture bazy danych
#otworz terminal i jednorazowo przy projekcie wpisz
#flask db init
#te komendy ponizej wykonaj za kazdym razem jak zmieni sie struktuta bazy (oraz podczas pierwszego tworzenia)
#flask db migrate
#flask db upgrade
class ContactForm(FlaskForm):
    name = TextField("Użytkownik")
    email = TextField("Adres email")
    subject = TextField("Temat wiadomości")
    message = TextAreaField("Wiadomość")
    submit = SubmitField("Wyślij")

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    email = ""
    name = ""
    passwd = ""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        passwd = request.form.get("passwd")
        dane = dict(request.form)
        with open("login_log.txt", "a") as f:
            f.write(dane["name"] + ";" + dane["email"] + ";" + current_time + "\n")
        #print(dane)
        # return f"Thanks, {request.form.get('name')}"
        #return render_template("login.html", message=f"Thanks, {dane['name']}")

        # success = True
        # if len(passwd) < 6:
        #     flash('length should be at least 6', category='danger')
        #     success = False
        #
        # if len(passwd) > 20:
        #     flash('length should be not be greater than 12', category='danger')
        #     success = False
        #
        # if not any(char.isdigit() for char in passwd):
        #     flash('Password should have at least one numeral', category='danger')
        #     success = False
        #
        # if not any(char.isupper() for char in passwd):
        #     flash('Password should have at least one uppercase letter', category='danger')
        #     success = False
        #
        # if not any(char.islower() for char in passwd):
        #     flash('Password should have at least one lowercase letter', category='danger')
        #     success = False
        #
        # if not any(True for char in passwd if char in punctuation):
        #     flash('Password should have at least one of the symbols $@#', category='danger')
        #     success = False
        #
        # if success:
        #     flash("Zalogowano!", category="success")

    return render_template('login.html', title='Login')

# @app.route("/register", methods=["GET", "POST"])
# def register():
#     def password_check(passwd):
#         SpecialSym = ['$', '@', '#', '%']
#         val = True
#
#         if len(passwd) < 6:
#             flash('length should be at least 6', 'error')
#             val = False
#
#         if len(passwd) > 20:
#             flash('length should be not be greater than 12', "error")
#             val = False
#
#         if not any(char.isdigit() for char in passwd):
#             print('Password should have at least one numeral', 'error')
#             val = False
#
#         if not any(char.isupper() for char in passwd):
#             print('Password should have at least one uppercase letter', 'error')
#             val = False
#
#         if not any(char.islower() for char in passwd):
#             print('Password should have at least one lowercase letter', 'error')
#             val = False
#
#         if not any(char in SpecialSym for char in passwd):
#             print('Password should have at least one of the symbols $@#', 'error')
#             val = False
#         if val:
#             return val
#
#     return render_template("register.html")
# # # Main method
# # def main():
# #     passwd = 'request.form.get("passwd")'
# #
# #     if (password_check(passwd)):
# #         print("Password is valid")
# #     else:
# #         print("Invalid Password !!")
# #
# #
# # # Driver Code
# # if __name__ == '__main__':
# #     main()
#
#
@app.route("/register", methods=["GET", "POST"])
def register():
    email = ""
    name = ""
    password1 = ""
    password2 = ""
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        success = True
        if len(password1) < 6:
            flash('length should be at least 6', category='danger')
            success = False

        if len(password1) > 12:
            flash('length should be not be greater than 12', category='danger')
            success = False

        if password2 == None:
            flash('confirm your password', category='danger')
            success = False

        if password1 != password2:
            flash('passwords must match', category='danger')
            success = False

        if not any(char.isdigit() for char in password1):
            flash('Password should have at least one numeral', category='danger')
            success = False

        if not any(char.isupper() for char in password1):
            flash('Password should have at least one uppercase letter', category='danger')
            success = False

        if not any(char.islower() for char in password1):
            flash('Password should have at least one lowercase letter', category='danger')
            success = False

        if not any(True for char in password1 if char in punctuation):
            flash('Password should have at least one of the symbols $@#', category='danger')
            success = False

        if success:
            flash("Zarejestrowano nowego użytkownika!", category="success")

        #return redirect(url_for('home'))
    return render_template("register.html", email=email, password1=password1, password2=password2, name=name)

@app.route('/contactus', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        wiadomosci = dict(request.form)
        with open("wiadomosci.txt", "a") as f:
            f.write(wiadomosci["name"] + ";" + wiadomosci["email"] + ";" + wiadomosci["email"] + current_time + "\n")
        flash("Dane zapisane", category="success")
    else:
        return render_template('contact_form.html', form=form)








# reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
#
#         # compiling regex
#         pat = re.compile(reg)
#
#         # searching regex
#         mat = re.search(pat, password1)
#
#         # validating conditions
#         if mat:
#             flash("Password is valid.", category="success")
#         else:
#             flash("Password invalid !!", category="danger")


# def register():
#     def main():
#         passwd = 'Geek12@'
#         reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
#
#         # compiling regex
#         pat = re.compile(reg)
#
#         # searching regex
#         mat = re.search(pat, passwd)
#
#         # validating conditions
#         if mat:
#             print("Password is valid.")
#         else:
#             print("Password invalid !!")

# return render_template("login.html")




