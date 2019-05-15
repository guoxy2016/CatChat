from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user, login_user

from ..extensions import db
from ..utils import flash_errors
from ..models import User
from ..form import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat.index'))
    if request.method == 'POST':
        form = LoginForm()
        if not form.validate():
            flash_errors(form)
            return render_template('auth/login.html')
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user is not None and user.validate_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('chat.index'))
        flash('用户名或密码错误!')
        return render_template('auth/login.html')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('chat.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat.index'))
    if request.method == 'POST':
        form = RegisterForm()
        if not form.validate():
            flash_errors(form)
            return render_template('auth/register.html')
        user = User(email=form.email.data.lower(), nickname=form.nickname.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('.login'))
    return render_template('auth/register.html')
