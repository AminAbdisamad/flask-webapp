from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os
from Forms import RegistrationForm, LoginForm


app = Flask(__name__)

# Create a secret key which will be used for hidden_tag() to protect agains CSRF attacks
load_dotenv()
secretKey = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = secretKey

posts = [
    {
        "title": "My App",
        "description": "Flask is micro-framework used for testing",
        "author": "Amin",
    },
    {
        "title": "Why Pyton",
        "description": "Python is multipurpose programming language that could be used wide range of areas from scripting to machine learning and robotics",
        "author": "Nasruddin",
    },
    {
        "title": "Why Javascript",
        "description": "Javascript is language that runs the entire web",
        "author": "Nasir",
    },
]

# Index Page
@app.route("/")
def index():
    return render_template("index.html", posts=posts)


# About Page
@app.route("/about")
def about():
    return render_template("about.html")


# Registration Page
@app.route("/register", methods=["GET", "POST"])
def register():
    register = RegistrationForm()
    if register.validate_on_submit():
        flash(f"Account created for {register.username.data}", "success")
        return redirect(url_for("index"))
    return render_template("register.html", title="Register Form", register=register)


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    login = LoginForm()
    return render_template("login.html", title="Login Form", login=login)


if __name__ == "__main__":
    app.run(debug=True)
