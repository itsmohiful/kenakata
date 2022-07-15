from flask_login import UserMixin

from kenakata import bcrypt, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    name = db.Column(db.String(length=200), nullable=True)
    price = db.Column(db.String(length=10), nullable=True)
    barcode = db.Column(db.String(length=12), nullable=True)
    description = db.Column(db.String(length=1000),nullable=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    

    def __repr__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=30), unique=True, nullable=False)
    password = db.Column(db.String(length=30), nullable=False)
    budget = db.Column(db.Integer(), nullable=True, default=1000)
    products = db.relationship('Product', backref='owned_user', lazy=True)
    

    @property
    def budget_prettify(self):
        if len(str(self.budget)) >= 4:
            return f'{ str(self.budget)[:-3] },{ str(self.budget)[-3:]}$'
        else:
            return 'f{self.budget}$'

    # @property
    # def password(self):
    #     return self.password

    # @password.setter
    # def password(self, plain_text_password):
    #     self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)
