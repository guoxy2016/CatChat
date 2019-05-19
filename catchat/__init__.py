import os
import random

import click
from flask import Flask, render_template

from .blueprints import *
from .extensions import db, login_manager, csrf, moment, socketio, oauth
from .models import Message, User


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    from .settings import config
    app = Flask('catchat')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprint(app)
    register_shell_contexts(app)
    register_template_contexts(app)
    register_errors(app)
    register_commands(app)

    return app


def register_logging(app=None):
    pass


def register_extensions(app=None):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)
    socketio.init_app(app)
    oauth.init_app(app)


def register_blueprint(app=None):
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(oauth_bp)
    app.register_blueprint(admin_bp)


def register_shell_contexts(app=None):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Message=Message)


def register_template_contexts(app=None):
    pass


def register_errors(app=None):
    @app.errorhandler(400)
    def bad_require(e):
        return render_template('errors.html', code=e.code, name=e.name, description=e.description)


def register_commands(app=None):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='清空')
    def init_db(drop):
        """初始化数据库"""
        if drop:
            click.confirm('确定要删除数据库内容吗?', abort=True)
            click.echo('删除数据库内容')
            db.drop_all()
        click.echo('创建数据库内容')
        db.create_all()
        click.echo('Done!')

    @app.cli.command()
    @click.option('--user', default=50, help='用户数量')
    @click.option('--message', default=500, help='消息数量')
    def forge(user, message):
        """虚拟数量"""
        from faker import Faker
        from sqlalchemy.exc import IntegrityError

        fake = Faker('zh-CN')
        click.echo('Initializing database...')
        db.drop_all()
        db.create_all()

        click.echo('Generic Admin...')
        admin = User(nickname='guoxy2016', email='1344166268@qq.com', github='https://github.com/guoxy2016')
        admin.password = '12345678'
        db.session.add(admin)
        db.session.commit()

        click.echo('Generic %d user' % user)
        for i in range(user):
            user = User(nickname=fake.user_name(), email=fake.email(), website=fake.url(),
                        github='https://github.com/%s' % fake.user_name(), bio=fake.sentence())
            user.password = '12345678'
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

        click.echo('Generic %d message' % message)
        for j in range(message):
            message = Message(body=fake.sentence(), timestamp=fake.date_time_this_year(),
                              author=User.query.get(random.randint(1, User.query.count())))
            db.session.add(message)
        db.session.commit()
        click.echo('Done!')
