from flask import url_for

from catchat.extensions import db
from catchat.models import User
from .base import BaseTestCase


class AuthTestCase(BaseTestCase):
    def setUp(self) -> None:
        super(AuthTestCase, self).setUp()
        user = User(email='third@catchat.com')
        db.session.add(user)
        db.session.commit()

    def test_login(self):
        response = self.client.get(url_for('auth.login'))
        self.assertIn('email', response.get_data(as_text=True))
        self.assertIn('密码', response.get_data(as_text=True))

        response = self.login('error@catchat.com', '123123123')
        data = response.get_data(as_text=True)
        self.assertNotIn('将内容写在这里, 并按Enter键发送', data)
        self.assertIn('用户名或密码错误', data)

        response = self.login('third@catchat.com')
        data = response.get_data(as_text=True)
        self.assertIn('请使用第三方登陆', data)

        response = self.login()
        data = response.get_data(as_text=True)
        self.assertIn('将内容写在这里, 并按Enter键发送', data)

    def test_logout(self):
        self.login()
        response = self.logout()
        self.assertIn("登陆", response.get_data(as_text=True))
        self.assertIn('注册', response.get_data(as_text=True))
    
    def test_register(self):
        response = self.client.get(url_for('auth.register'))
        self.assertIn('昵称', response.get_data(as_text=True))
        self.assertIn('Email', response.get_data(as_text=True))
        self.assertIn('确认密码', response.get_data(as_text=True))

        response = self.client.post(url_for('auth.register'), data=dict(
            nickname='zhangsan',
            email='zhangsan@catchat.com',
            password='12345678',
            password2='12345678',
            terms=True
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('注册成功', data)
        self.assertIsNotNone(User.query.filter_by(email='zhangsan@catchat.com').first())
