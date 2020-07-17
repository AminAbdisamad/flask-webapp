import os
import secrets
from PIL import Image
from flask import render_template, redirect, url_for, flash, request
from flaskapp.Forms import RegistrationForm, LoginForm, UpdateAccountForm, CreatePost
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
@app.route("/", methods=["GET", "POST"])
def index():
    # entities = MyEntity.query.order_by(desc(MyEntity.time)).limit(3).all()
    posts = Post.query.order_by(Post.datePosted.desc()).all()
    form = CreatePost()
    if form.validate_on_submit():
        post = Post(content=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post Created Successfully", "is-success")
        return redirect(url_for("index"))
    return render_template("index.html", form=form, posts=posts)


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
            return redirect(nextPage) if nextPage else redirect(url_for("index"))
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


# Save User Profile Picture
def saveUserPicture(picture):
    # We use hexa for profile picture name, if we use names there could be image with same filename
    randomHex = secrets.token_hex(8)
    # We explit filename and extension
    _, fileExtension = os.path.splitext(picture.filename)
    # concatinate hexa and file Extension something like [dfjdshf234.png]
    pictureName = randomHex + fileExtension
    picturePath = os.path.join(app.root_path, "static/profile_pictures", pictureName)
    # Lets resize Image before Storing
    imageSize = (125, 125)
    image = Image.open(picture)
    image.thumbnail(imageSize)
    image.save(picturePath)
    # picture.save(picturePath)
    return pictureName


# User Account
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    imageFilter = url_for(
        "static", filename="profile_pictures/" + current_user.image_file
    )
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            imageFile = saveUserPicture(form.picture.data)
            current_user.image_file = imageFile
        current_user.username = form.username.data
        current_user.email = form.email.data
        # Update Account with new information such as name,bio and location
        user = User.query.filter_by(username=current_user.username).update(
            dict(name=form.name.data, location=form.location.data, bio=form.bio.data)
        )

        db.session.commit()
        flash("Your Account has been updated successfully", "is-success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.location.data = current_user.location
        form.bio.data = current_user.bio
    return render_template(
        "account.html",
        title="User Account",
        userProfile=imageFilter,
        form=form,
        pictureName=form.picture.data,
    )

