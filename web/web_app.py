from flask import Flask, flash, redirect, render_template, url_for, request
from functools import wraps
app = Flask(__name__)

app.secret_key = 'better work'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route("/")
def welcome():
    return render_template("welcome.html")

def home():
	return render_template("index.html")

@app.route("/login", methods =["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Invalid username or password. please try again!"
        else:
            session["logged_in"] = True
            flash("You were logged in.")
            return redirect(url_for("index.html"))
    return render_template("login.html", error=error)

@app.route("/sensors.html")
def sensors():
    return "Sensors"

@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None)
    flash("you were logged out")
    return redirect(url_for("/welcome)"))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)