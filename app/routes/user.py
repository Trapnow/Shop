from flask import Blueprint, redirect, render_template, url_for, request

from flask_login import login_user, logout_user
from ..functions import save_picture
from ..forms import RegistrationForm, LoginForm
from ..extensions import db, bcrypt
from ..models.user import User

user = Blueprint("user", __name__)


@user.route("/user/registration", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        if form.avatar.data:
            avatar_filename = save_picture(form.avatar.data)
        else:
            avatar_filename = 'img/default.jpg'
        user = User(name=form.name.data, avatar=avatar_filename, email=form.email.data, phone=form.phone.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("user.login"))
    return render_template("registration.html", form=form)


@user.route("/user/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("book.index"))
    return render_template("login.html", form=form)


@user.route("/user/logout", methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for("book.index"))
