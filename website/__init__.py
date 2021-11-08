import flask
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy #0. Instalacja i import SQLAlchemy (requirements.txt)
import pandas as pd
from flask_migrate import Migrate
from sqlalchemy import ForeignKey
from .forms import ComplainForm, ContactForm, RegisterForm, LoginForm
from werkzeug.security import generate_password_hash

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(current_time)
dzisiaj = date.today()
print(dzisiaj)


app = Flask(__name__)
app.secret_key = 'dupa'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" #1 Dodanie info o rodzaju bazy i gdzie jest
db = SQLAlchemy(app=app) #2. Dodanie obiektu

#3. stworzenie modelu/tabeli
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(25))
    user_email = db.Column(db.String(35), unique=True)
    user_password = db.Column(db.String(25))
    user_project = db.Column(db.String(50))
    user_login_log = db.Column(db.String(50))
    user_complain = db.Column(db.String(250))
    user_message = db.column(db.String(250))

class Complains(db.Model):
    complain_id = db.Column(db.Integer, primary_key=True)
    complain_author = db.Column(db.Integer)
    complain_subject = db.Column(db.String(50))
    complain_body = db.Column(db.String(255))

class Projects(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(25), unique=True)
    project_members = db.Column(db.Integer)
    project_description = db.Column(db.String(255))


class Storage(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    article_code = db.Column(db.String(20), unique=True)
    article_name = db.Column(db.String(50))
    article_lot_number = db.Column(db.String(20), unique=True)
    article_purchase_date = db.Column(db.Integer)
    article_purchase_user = db.Column(db.Integer)
    article_delivery_date = db.Column(db.Integer)
    article_delivery_quantity = db.Column(db.Integer)
    article_units = db.Column(db.String(10))
    article_initial_quantity = db.Column(db.Integer)
    article_used = db.Column(db.Integer)
    article_user = db.Column(db.Integer)
    article_remaining_quantity = db.Column(db.Integer)
    article_project = db.Column(db.Integer)


class Messages(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    message_author = db.Column(db.String(35))
    message_subject = db.Column(db.String(50))
    message_body = db.Column(db.String(255))


class Login_log(db.Model):
    login_log_id = db.Column(db.Integer, primary_key=True)
    login_user = db.Column(db.String(35))
    login_date = db.Column(db.String(12))
    login_time = db.Column(db.String(12))



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
        passwd = request.form.get("password1")
        dane = dict(request.form)
        with open("login_log.txt", "a") as f:
            f.write(dane["email"] + " ; " + str(dzisiaj) + " ; " + current_time + "\n")
        login_log = Login_log(login_user=email, login_date=dzisiaj, login_time=current_time)
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
        kontakt = Messages(message_author=email, message_subject=subject, message_body=message)
        db.session.add(kontakt)
        db.session.commit()
        flash("Wiadomość została wysłana", category="success")
    return render_template('contact_form.html', form=form)


@app.route("/complain", methods=["GET", "POST"])
def complain():
    form = ComplainForm()
    if request.method == "POST":
        email = request.form["email"]
        complain = request.form["complain"]

    if form.validate_on_submit():
        #print(f"{form.email.data} {form.complain.data}")
        flash("Dodano Twoją skargę", category="success")
    else:
        for error in list(form.email.errors) + list(form.complain.errors):
            flash(error, category="danger")

        skarga = Complains(complain_author=email, complain_body=complain)
        db.session.add(skarga)
        db.session.commit()
        flash("Dodano Twoją skargę", category="success")
    return render_template("complain.html", form=form)






