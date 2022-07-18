from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from kenakata import app, bcrypt, db
from kenakata.forms import (LoginForm, ProductForm, ProfileUpdateForm,
                            RegisterForm)
from kenakata.models import Product, User
from kenakata.utils import save_picture, save_product_picture


@app.route("/")
@app.route("/home")
def home():
    products = Product.query.all()

    return render_template("home.html",products=products,title='Home page')


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


@app.route('/add-new-product', methods=['GET','POST'])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        image_file = save_product_picture(form.image.data)

        product = Product(name=form.name.data, price=form.price.data, barcode=form.barcode.data, description=form.description.data,owned_user=current_user, image=image_file)

        db.session.add(product)
        db.session.commit()

        flash('New Product has been created!', 'success')
        return redirect(url_for('home'))

    return render_template("create-product.html", form=form, title='Add new product')


@app.route('/product-detail/<int:product_id>')
def product_detail(product_id):
    product = Product.query.filter_by(id=product_id).first()
    return render_template("product-details.html", product=product, title='product details')






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



@app.route('/user-profile')
@login_required
def user_profile():
    return render_template("profile.html", title='User Profile')



@app.route('/profile-update',methods=['GET', 'POST'])
@login_required
def profile_update():
    form = ProfileUpdateForm()

    if form.validate_on_submit():
        if form.image.data:
            image_file = save_picture(form.image.data)
            current_user.image = image_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.mobile = form.mobile.data
        current_user.budget = form.budget.data

        db.session.commit()
        flash('Profiel update successfully', 'success')
        return redirect(url_for('user_profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        if current_user.mobile:
            form.mobile.data = current_user.mobile
        if current_user.budget:
            form.budget.data = current_user.budget
        form.image.data = url_for('static', filename='profile_images/' + current_user.image)

    return render_template("profile-update.html", form=form, title='Profile Update')
