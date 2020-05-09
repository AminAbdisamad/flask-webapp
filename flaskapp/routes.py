from flask import render_template, redirect, url_for, flash, request
from flaskapp.Forms import RegistrationForm, LoginForm
from flaskapp.models.User import User
from flaskapp.models.Post import Post
from flaskapp import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        "title": "My App",
        "description": "Flask is micro-framework used for testing",
        "author": "Amin",
    },
    {
        "title": "Why Pyton",
        "description": "Python is multipurpose programming language that could ",
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
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    register = RegistrationForm()
    if register.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(register.password.data).decode(
            "utf-8"
        )
        user = User(
            username=register.username.data,
            email=register.email.data,
            password=hashedPassword,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Your Account has been create and now you can loggin", "is-success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register Form", register=register)


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    login = LoginForm()
    if login.validate_on_submit():
        user = User.query.filter_by(email=login.email.data).first()
        # Validate user
        if user and bcrypt.check_password_hash(user.password, login.password.data):
            login_user(user, remember=login.remember.data)
            # if we have params in the url we should redirect automatically
            nextPage = request.args.get("next")
            flash("Sucessfully Logged In", "is-success")
            return redirect(nextPage) if nextPage else (url_for("index"))
        else:
            flash(
                "Loggin Unsuccessfull, please check your email and password",
                "is-danger",
            )
    return render_template("login.html", title="Login Form", login=login)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="User Account")
