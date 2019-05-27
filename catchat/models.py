import hashlib
from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128))
    _email_hash = db.Column(db.String(128))
    nickname = db.Column(db.String(30), nullable=True)
    website = db.Column(db.String(255))
    github = db.Column(db.String(255))
    bio = db.Column(db.String(120))
    messages = db.relationship('Message', back_populates='author', cascade='all')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.generate_email_hash()

    def generate_email_hash(self):
        if self.email is not None and self._email_hash is None:
            self._email_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('Not readable!')

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self._password_hash, password)

    @property
    def gravatar(self):
        return 'https://gravatar.com/avatar/%s?d=wavatar' % self._email_hash

    @property
    def is_admin(self):
        return self.email == current_app.config['CATCHAT_ADMIN_EMAIL']


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='messages')
