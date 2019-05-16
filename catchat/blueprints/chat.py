from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from flask_socketio import emit

from ..extensions import db, socketio
from ..form import ProfileForm
from ..models import Message, User
from ..utils import flash_errors

chat_bp = Blueprint('chat', __name__)
online_users = []


@chat_bp.route('/')
def index():
    messages = Message.query.order_by(Message.timestamp.asc())
    user_amount = User.query.count()
    return render_template('chat/index.html', messages=messages, user_amount=user_amount)


@chat_bp.route('/anonymous')
def anonymous():
    return render_template('chat/anonymous.html')


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


@socketio.on('new message')
def new_message(message_body):
    message = Message(body=message_body, author=current_user._get_current_object())
    db.session.add(message)
    db.session.commit()
    emit('new message',
         {'message_html': render_template('chat/_message.html', message=message)},
         broadcast=True)


@socketio.on('connect')
def connect():
    global online_users
    if current_user.is_authenticated and current_user.id not in online_users:
        online_users.append(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)


@socketio.on('disconnect')
def disconnect():
    global online_users
    if current_user.is_authenticated and current_user.id in online_users:
        online_users.remove(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)


@socketio.on('new message', namespace='/anonymous')
def new_anonymous_message(message_body):
    avatar = 'https://www.gravatar.com/avatar?d=mm'
    nickname = '匿名'
    emit('new message',
         {'message_html': render_template('chat/_anonymous_message.html', message=message_body, avatar=avatar,
                                          nickname=nickname)},
         broadcast=True, namespace='/anonymous')
