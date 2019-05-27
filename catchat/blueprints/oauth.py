import os

from flask import Blueprint, abort, redirect, url_for, flash
from flask_login import current_user, login_user

from ..extensions import oauth, db
from ..models import User

oauth_bp = Blueprint('oauth', __name__)

github = oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    api_base_url='https://api.github.com/',
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_methods='POST',
)

providers = {
    'github': github,
}

profile_endpoints = {
    'github': 'user',
}


@oauth_bp.route('/login/<provider_name>')
def oauth_login(provider_name):
    if provider_name not in providers:
        abort(404)

    if current_user.is_authenticated:
        return redirect('chat.index')
    callback = url_for('.oauth_callback', provider_name=provider_name, _external=True)
    return providers[provider_name].authorize_redirect(callback)


@oauth_bp.route('/callback/<provider_name>')
def oauth_callback(provider_name):
    if provider_name not in providers:
        abort(404)
    provider = providers[provider_name]
    response = provider.authorize_access_token()
    if response is not None:
        access_token = response.get('access_token')
    else:
        access_token = None
    if access_token is None:
        flash('认证失败, 请稍候重试!')
        return redirect('auth.login')
    profile_endpoint = profile_endpoints[provider_name]
    response = provider.get(profile_endpoint)
    response = response.json()
    username = response.get('name')
    website = response.get('blog')
    github = response.get('html_url')
    email = response.get('email')
    bio = response.get('bio')
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(email=email, nickname=username, website=website, github=github, bio=bio)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('chat.profile'))
    login_user(user, remember=True)
    return redirect(url_for('chat.index'))
