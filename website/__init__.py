from flask import Flask, render_template, redirect, url_for, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy  # 0. Instalacja i import SQLAlchemy (requirements.txt)
from flask_migrate import Migrate
from sqlalchemy.sql.functions import user

from .forms import ComplaintForm, ContactForm, RegisterForm, LoginForm, ForgotForm, ResetForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required  # L1. importy
from flask_mail import Message, Mail
from random import choice
from string import ascii_letters
import requests

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(current_time)


def create_code(size):
    return "".join([choice(ascii_letters) for i in range(size)])


app = Flask(__name__)
app.secret_key = 'dupa'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"  # 1 Dodanie info o rodzaju bazy i gdzie jest
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "sanczo.panczo77@gmail.com"
app.config["MAIL_PASSWORD"] = "lbbadatqttyykesf"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail = Mail(app=app)
db = SQLAlchemy(app=app)  # 2. Dodanie obiektu


# 3. stworzenie modelu/tabeli
class User(db.Model, UserMixin):  # L2. UserMixin - dodajac go do tabeli mowimy ze ta tabela bedzie mogla byc
    # odczytywana przez LoginManagera
    id = db.Column(db.Integer, primary_key=True)
    user_first_name = db.Column(db.String(25))
    user_second_name = db.Column(db.String(35))
    user_company_initials = db.Column(db.String(4))
    user_password = db.Column(db.String(25))
    user_email = db.Column(db.String(35), unique=True, nullable=False)
    user_project = db.Column(db.String(50), db.ForeignKey('projects.project_id'))
    user_login_log = db.Column(db.String(50), db.ForeignKey('login.login_log_id'))
    user_complaint = db.Column(db.Text, db.ForeignKey('complaints.complaint_id'))
    user_message = db.column(db.Text, db.ForeignKey('messages.message_id'))
    is_confirmed = db.Column(db.Boolean, default=False)
    confirmation_code = db.Column(db.String(65))


class Messages(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    message_author = db.Column(db.String(35), db.ForeignKey('user.id'), nullable=False)
    #  me_author = db.relationship('User', backref=db.backref('messages', lazy=True))
    message_subject = db.Column(db.String(50))
    message_body = db.Column(db.Text, nullable=False)
    message_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow())


class Complaints(db.Model):
    complaint_id = db.Column(db.Integer, primary_key=True)
    complaint_author = db.Column(db.String(35), db.ForeignKey('user.user_email'), nullable=False)
    complaint_subject = db.Column(db.String(50))
    complaint_body = db.Column(db.Text, nullable=False)
    #  author = db.relationship('User', backref=db.backref('complaints', lazy=True))


class Login(db.Model):
    login_log_id = db.Column(db.Integer, primary_key=True)
    login_user_id = db.Column(db.String(35), db.ForeignKey("user.id"), nullable=False)
    # lo_user = db.relationship('User', backref=db.backref('logins', lazy=True))
    login_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow())


class Projects(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(25), unique=True)
    project_members = db.Column(db.String(35), db.ForeignKey("user.id"), nullable=False)
    # pr_members = db.relationship('User', backref=db.backref('projects', lazy=True))
    project_description = db.Column(db.String(255))


class Storage(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    article_code = db.Column(db.String(20), unique=True)
    article_name = db.Column(db.String(50))
    article_lot_number = db.Column(db.String(20), unique=True)
    article_purchase_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    article_purchase_user = db.Column(db.String(35), db.ForeignKey("user.id"), nullable=False)
    article_delivery_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    article_delivery_quantity = db.Column(db.Integer)
    article_units = db.Column(db.String(10))
    article_initial_quantity = db.Column(db.Integer)
    article_used = db.Column(db.Integer)
    article_user = db.Column(db.String(35), db.ForeignKey("user.user_email"), nullable=False)
    article_remaining_quantity = db.Column(db.Integer)
    article_project = db.Column(db.String(35), db.ForeignKey("projects.project_id"), nullable=False)
    # user = db.relationship('User', backref=db.backref('articles', lazy=True))
    # project = db.relationship('Projects', backref=db.backref('arts', lazy=True))


# 4. stworzenie obiektu migracji
migrate = Migrate(app=app, db=db)


# 5. Wykonanie migracji w terminalu
# Migracja - to skrypt ktory tworzy/modyfikuje strukture bazy danych
# otworz terminal i jednorazowo przy projekcie wpisz
# flask db init
# te komendy ponizej wykonaj za kazdym razem jak zmieni sie struktura bazy (oraz podczas pierwszego tworzenia)
# flask db migrate
# flask db upgrade

# L3. Utworz login managera
login_manager = LoginManager(app=app)
login_manager.login_view = "login"  # L4. wpisujemy nazwe funkcji do ktorej ma nas przekierowac jesli uzytkownik
# probuje wejsc w miejsce nie dla niego ;)
# L5, Musimy podac w jaki posob LoginManager ma pobierac uzytkownika z bazy


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/")
@login_required
def home():
    # msg = Message("Testowy temat", sender="Sanczo panczo", recipients=["weresa@gmail.com", "rork3@wp.pl"])
    # msg.html = "<h1>Witaj</h1>"
    # mail.send(msg)
    users = User.query.all()
    return render_template('home.html', users=users)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # utworz obiekt klasy-tabeli
        user = User(user_first_name=form.first_name.data,
                    user_second_name=form.second_name.data,
                    user_email=form.email.data,
                    user_password=generate_password_hash(form.password1.data, method="sha256"),
                    confirmation_code=create_code(64))
        db.session.add(user)
        db.session.commit()
        msg = Message("Potwierdzenie stworzenia konta", sender="Sanczo Panczo",
                      recipients=["rork3@wp.pl", user.user_email])
        msg.html = f"<h1>Witaj</h1> Tw??j link aktywacyjny: " \
                   f"<a href='http://127.0.0.1:5000/confirm/{user.confirmation_code}'>CLICK</a>"
        mail.send(msg)
        flash("Zarejestrowano nowego u??ytkownika!", category="success")
        print(msg.html)
        return redirect(url_for("login"))
    else:
        for error in list(form.email.errors) + list(form.password1.errors):
            flash(error, category="danger")

    return render_template("register.html", form=form)


@app.route("/confirm/<code>")
def confirm(code):
    user = User.query.filter_by(confirmation_code=code).first()
    if not user:
        return "<h1>Bad Request</h1>", 400
    user.confirmation_code = ""
    user.is_confirmed = True
    db.session.commit()
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(user_email=email).first()
        if user:
            if check_password_hash(user.user_password, password):
                if user.is_confirmed:
                    login_log = Login(login_user_id=user.id, login_date=datetime.now())
                    db.session.add(login_log)
                    db.session.commit()
                    login_user(user)  # dodaj to zeby sie user zalogowal
                    flash("Zalogowano!", category="success")
                    return redirect(url_for("home"))
                else:
                    flash("Email nie zosta?? potwierdzony", category="danger")
            else:
                flash("Niepoprawne haslo!", category="danger")
        else:
            flash("Nie ma takiego uzytkownika!", category="danger")

    return render_template('login.html', title='Login', form=form)


@app.route('/contactus', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        kontakt = Messages(message_author=form.email.data, message_subject=form.subject.data,
                           message_body=form.message.data)
        db.session.add(kontakt)
        db.session.commit()
        flash("Wiadomo???? zosta??a wys??ana", category="success")
    # else:
    #     for err in form.email.errors:
    #         flash(err, category="danger")
    return render_template('contact_form.html', form=form)


@app.route("/complain", methods=["GET", "POST"])
@login_required  # dodaj to do kazdej strony ktora ma byc dostepna tylko po zalogowaniu
def complaint():
    form = ComplaintForm()
    if form.validate_on_submit():
        skarga = Complaints(complaint_author=form.email.data, complaint_body=form.complaint.data)
        db.session.add(skarga)
        db.session.commit()
        flash("Dodano Twoj?? skarg??", category="success")
    else:
        for error in list(form.email.errors) + list(form.complaint.errors):
            flash(error, category="danger")

    return render_template("complaint.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/forgot', methods=["GET", "POST"])
def forgot():
    form = ForgotForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if user:
            msg = Message("Potwierdzenie stworzenia konta", sender="Sanczo Panczo",
                          recipients=["rork3@wp.pl", user.user_email])
            msg.html = f"<h1>Witaj</h1> Tw??j link do resetu hasla: " \
                       f"<a href='http://127.0.0.1:5000/confirm/{user.confirmation_code}'>CLICK</a>"
            mail.send(msg)
            flash("Wiadomosc wyslana!", category="success")
        else:
            flash("Nie ma uzytkownika o takim adresie email", category="danger")
    return render_template('forgot.html', form=form)


@app.route('/reset', methods=["GET", "POST"])
def reset():
    form = ResetForm()
    if form.validate_on_submit():
        if check_password_hash(User.user_password, password):
            if user.is_confirmed:
                nowe_haslo = User(user_password=generate_password_hash(form.password_new.data, method="sha256"))
                db.session.add(nowe_haslo)
                db.session.commit()
                login_user(user)  # dodaj to zeby sie user zalogowal
                flash("Zalogowano!", category="success")
                return redirect(url_for("home"))

    return render_template('reset.html', form=form)


@app.route("/games")
def games():
    data = requests.get("https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=1000").json()
    return render_template("games.html", data=data)
