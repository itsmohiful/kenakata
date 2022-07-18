from crypt import methods

from flask import flash, redirect, render_template, url_for
from flask_login import login_user, logout_user

from kenakata import app, bcrypt, db
from kenakata.forms import LoginForm, RegisterForm
from kenakata.models import Product, User


@app.route("/")
@app.route("/home")
def home():
    products = Product.query.all()

    return render_template("home.html",products=products)

@app.route('/product-detail')
def product_detail():
    return render_template("product-details.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password1.data).decode("utf-8")
        user = User(username=form.username.data,
        email=form.email.data,password=hashed_password)

        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'Account has been created and Login as: {user.username}', category='success')
        return redirect(url_for('home'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Something wrong! {err_msg}',category='danger')

    return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'You are login as: {user.username}', category='success')
            return redirect(url_for('home'))
        else:
            flash('Username or Password are not matche! Please try again', category='danger')

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been log out!',category='success')
    return redirect(url_for('login'))
