from flask_wtf import FlaskForm
from wtforms import (IntegerField, PasswordField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

from kenakata.models import User


class ProductForm(FlaskForm):
    name = StringField(label='Product Name', validators=[Length(max=300), DataRequired()])
    price = IntegerField(label='Product Price', validators=[DataRequired()])
    barcode = StringField(label='Barcode', validators=[Length(max=15),DataRequired()])
    description = TextAreaField(label='Product Details', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class RegisterForm(FlaskForm):

    def validate_username(self,username):
        print(f'validates: {username}')
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username alredy exists!')

    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email alredy exists!')

    username = StringField(label='Username', validators=[Length(min=2,max=30), DataRequired()])
    email = StringField(label='Email Address',validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Sign Up')



class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')
