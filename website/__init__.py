from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

app = Flask(__name__)
app.secret_key = 'dupa'

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
    if len(passwd) < 6:
        flash('length should be at least 6')

    elif len(passwd) > 20:
        print('length should be not be greater than 12')

    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeral')

    if not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')

    if not any(char.islower() for char in passwd):
        print('Password should have at least one lowercase letter')

    if not any(char in SpecialSym for char in passwd):
        print('Password should have at least one of the symbols $@#')

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
# #     passwd = 'Geek12@'
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

    if "@" not in email:
        flash("Podaj poprawny adres email", category="danger")
    elif len(email) < 2:
        flash("Email za krotki", category="danger")
    elif len(name) < 2:
        flash("Nazwa za krotka", category="danger")
    elif len(password1) < 4:
        flash("Haslo powinno zawiera przynajmniej 4 znaki", category="danger")
    elif password1 != password2:
        flash("Hasla nie sa takie same", category="danger")
    else:
        flash( "Utworzono uzytkownika", category="success")
        return redirect(url_for('home'))

    return render_template("register.html", email=email, password1=password1, password2=password2, name=name)












def register():
    def main():
        passwd = 'Geek12@'
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

        # compiling regex
        pat = re.compile(reg)

        # searching regex
        mat = re.search(pat, passwd)

        # validating conditions
        if mat:
            print("Password is valid.")
        else:
            print("Password invalid !!")

    return render_template("login.html")




