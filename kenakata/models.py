from email.policy import default

from flask_login import UserMixin

from kenakata import bcrypt, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    name = db.Column(db.String(length=200), nullable=True)
    price = db.Column(db.String(length=10), nullable=True)
    image = db.Column(db.String(length=40), nullable=True,default='default.jpg')
    barcode = db.Column(db.String(length=12), nullable=True)
    description = db.Column(db.String(length=1000),nullable=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    

    def __repr__(self):
        return self.name

    def buy(self, user):
        self.owner = user.id
        user.budget -= int(self.price)
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget +=int(self.price)
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=30), unique=True, nullable=False)
    password = db.Column(db.String(length=30), nullable=False)
    image = db.Column(db.String(length=40), nullable=True,default='default.jpg')
    mobile = db.Column(db.String(length=20),nullable=True)
    budget = db.Column(db.Integer(), nullable=True, default=1000)
    products = db.relationship('Product', backref='owned_user', lazy=True)
    

    @property
    def budget_prettify(self):
        if len(str(self.budget)) >= 4:
            return f'{ str(self.budget)[:-3] },{ str(self.budget)[-3:]} $'
        else:
            return f'{self.budget} $'


    def can_purchase(self, product_obj):
        return self.budget >= int(product_obj.price)

    def can_sell(self, product_obj):
        return product_obj in self.products

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)
