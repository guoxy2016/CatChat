from .auth import auth_bp
from .chat import chat_bp
from .oauth import oauth_bp
from .admin import admin_bp

__all__ = ['auth_bp', 'chat_bp', 'oauth_bp', 'admin_bp']
