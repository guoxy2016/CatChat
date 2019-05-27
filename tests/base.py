from unittest import TestCase

from flask import url_for

from catchat import create_app
from catchat.extensions import db
from catchat.models import User, Message


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        app = create_app('testing')
        self.context = app.test_request_context()  # 为了url_for()的正常使用需要注册请求上下文
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()
        user = User(email='admin@catchat.com', nickname='guoxy2016')
        user.password = '12345678'
        message = Message(body='Test Message 1', author=user)

        normal_user = User(email='normal@catchat.com', nickname='normal_user')
        normal_user.password = '12345678'
        db.session.add_all([message, normal_user])
        db.session.commit()

    def tearDown(self) -> None:
        db.drop_all()
        self.context.pop()

    def login(self, email='admin@catchat.com', password='12345678'):
        return self.client.post(url_for('auth.login'), data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)
