from flask import Blueprint, render_template, redirect, url_for, flash, request
from . import db, login_manager
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"].lower().strip()
        password = request.form["password"]
        name = request.form.get("full_name", "")
        if User.query.filter_by(email=email).first():
            flash("Email already registered", "danger")
            return redirect(url_for("auth.signup"))
        u = User(email=email, full_name=name, password_hash=generate_password_hash(password))
        db.session.add(u)
        db.session.commit()
        flash("Account created. Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("signup.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].lower().strip()
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid credentials", "danger")
            return redirect(url_for("auth.login"))
        login_user(user)
        flash("Logged in", "success")
        next_page = request.args.get("next") or url_for("main.dashboard")
        return redirect(next_page)
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for("main.home"))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
