from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dupa'

@app.route("/", methods=["GET", "POST"])
def home():
    user = {'username': 'Wiktor'}
    return render_template('home.html', title='Home', user=user)







