from crypt import methods
from turtle import title

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from kenakata import app, bcrypt, db
from kenakata.forms import LoginForm, RegisterForm
from kenakata.models import Product, User


@app.route("/")
@app.route("/home")
def home():
    products = Product.query.all()

    return render_template("home.html",products=products,title='Home page')


@app.route('/product-detail')
def product_detail():
    return render_template("product-details.html", title='product details')


@app.route('/product-purchase/<int:product_id>', methods=['POST'])
def product_purchase(product_id):
    if request.method == 'POST':
        product = Product.query.filter_by(id=product_id).first()
        if product:
            if current_user.can_purchase(product):
                product.buy(current_user)
                flash(f"Congratulations! You purchased {product.name} for {product.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {product.name}!", category='danger')

    return redirect(url_for('home'))


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

    return render_template("register.html", form=form, title='Register Account')


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

    return render_template("login.html", form=form, title='Sign In')


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been log out!',category='success')
    return redirect(url_for('login'))
