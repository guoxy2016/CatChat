from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, URL, Email, EqualTo, Length, ValidationError, Optional

from .models import User


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email(), Length(1, 254)])
    password = PasswordField(validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField()


class RegisterForm(FlaskForm):
    nickname = StringField(validators=[DataRequired(), Length(3, 30)])
    email = StringField(validators=[DataRequired(), Email(), Length(1, 254)])
    password = PasswordField(validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField(validators=[DataRequired(), Length(8, 128)])
    terms = BooleanField(validators=[DataRequired()])

    def validate_terms(self, field):
        if not field.data:
            raise ValidationError('只有同意条款才能注册!')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('这个Email地址已经注册, 换一个试试吧.')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('这个昵称已被占用, 换一个试试吧.')


class ProfileForm(FlaskForm):
    nickname = StringField(validators=[DataRequired(), Length(3, 30)])
    github = StringField(validators=[Optional(), URL(), Length(0, 255)])
    website = StringField(validators=[Optional(), URL(), Length(0, 255)])
    bio = StringField(validators=[Optional(), Length(0, 120)])

    def validate_nickname(self, field):
        if current_user.nickname != field.data and User.query.filter_by(nickname=field.data).first():
            raise ValidationError('这个昵称已被占用, 换一个试试吧.')
