from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user

from ..extensions import db
from ..form import ProfileForm
from ..models import Message, User
from ..utils import flash_errors

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/')
def index():
    messages = Message.query.order_by(Message.timestamp.asc())
    user_amount = User.query.count()
    return render_template('chat/index.html', messages=messages, user_amount=user_amount)


@chat_bp.route('/profile/<user_id>')
def get_profile(user_id):
    user = User.query.get(user_id)
    return render_template('chat/_profile_card.html', user=user)


@chat_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        form = ProfileForm()
        if not form.validate():
            flash_errors(form)
            return render_template('chat/profile.html')
        current_user.nickname = form.nickname.data
        current_user.website = form.website.data
        current_user.github = form.github.data
        current_user.bio = form.bio.data
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('chat/profile.html')
