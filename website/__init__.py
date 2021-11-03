import flask
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, date
from string import punctuation
from flask_sqlalchemy import SQLAlchemy #0. Instalacja i import SQLAlchemy (requirements.txt)
import pandas as pd
from flask_migrate import Migrate
from sqlalchemy import ForeignKey

from .forms import ComplainForm, ContactForm, RegisterForm, LoginForm
from werkzeug.security import generate_password_hash

now = datetime.now()
dzisiaj = date.today()
current_time = now.strftime("%H:%M:%S")

app = Flask(__name__)
app.secret_key = 'dupa'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" #1 Dodanie info o rodzaju bazy i gdzie jest
db = SQLAlchemy(app=app) #2. Dodanie obiektu

#3. stworzenie modelu/tabeli

class Obieg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(10), unique=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    email = db.Column(db.String(35), unique=True)
    password = db.Column(db.String(25))
    obieg = db.Column(db.String(50), ForeignKey(Obieg.id))
    logowanie = db.Column(db.String(50))
    complain = db.Column(db.String(250))
    wiadomoscDoTworcy = db.column(db.String(250))

class Chemical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kod_towaru = db.Column(db.String(10), unique=True)
    nazwa = db.Column(db.String(25))
    opakowanie = db.Column(db.String(25))
    przychod = db.Column(db.Integer)
    rozchod = db.Column(db.Integer)
    stan_koncowy = db.Column(db.Integer)



#4. stworzenie obiektu migracji
migrate = Migrate(app=app, db=db)

#5. Wykonanie migracji w terminalu
#Migracja - to skrypt ktory tworzy/modyfikuje strukture bazy danych
#otworz terminal i jednorazowo przy projekcie wpisz
#flask db init
#te komendy ponizej wykonaj za kazdym razem jak zmieni sie struktura bazy (oraz podczas pierwszego tworzenia)
#flask db migrate
#flask db upgrade

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    email = ""
    name = ""
    passwd = ""
    if request.method == "POST":
        email = request.form.get("email")
        passwd = request.form.get("passwd")
        dane = dict(request.form)
        with open("login_log.txt", "a") as f:
            f.write(dane["email"] + " ; " + str(dzisiaj) + " ; " + current_time + "\n")
        login_log = User(logowanie=str(dzisiaj) + current_time)
        db.session.add(login_log)
        db.session.commit()
        flash("Zalogowano!", category="success")

    return render_template('login.html', title='Login')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(f"{form.name.data} {form.email.data}")
        flash("Rejestracja poprawna", category="success")
    else:
        for error in list(form.email.errors) + list(form.password1.errors):
            flash(error, category="danger")

            # utworz obiekt klasy-tabeli
            user = User(name=name, email=email, password=generate_password_hash(password1, method="sha256"))
            db.session.add(user)
            db.session.commit()
            flash("Zarejestrowano nowego użytkownika!", category="success")

        #return redirect(url_for('home'))
    return render_template("register.html")

@app.route('/contactus', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        wiadomosci = pd.DataFrame({'name': name, 'email':email, 'subject': subject, 'message': message}, index = [0])
        wiadomosci.to_csv('/home/sanczo/PycharmProjects/stronka/contactusMessage.csv')
        # with open("wiadomosci.txt", "a") as f:
            # f.write(wiadomosci["name"] + " ; " + wiadomosci["email"] + " ; " + str(dzisiaj) + " ; " + current_time + "\n")
        flash("Wiadomość została wysłana", category="success")
    return render_template('contact_form.html', form=form)


@app.route("/complain", methods=["GET", "POST"])
def complain():
    form = ComplainForm()
    if form.validate_on_submit():
        #print(f"{form.email.data} {form.complain.data}")
        flash("Dodano Twoją skargę", category="success")
    else:
        for error in list(form.email.errors) + list(form.complain.errors):
            flash(error, category="danger")

        # skarga = User(name=name, email=email, complain=complain)
        # db.session.add(skarga)
        # db.session.commit()
        #flash("Dodano Twoją skargę", category="success")
    return render_template("complain.html", form=form)






