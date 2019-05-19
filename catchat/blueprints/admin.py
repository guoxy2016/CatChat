from flask import Blueprint, abort
from flask_login import current_user

from ..extensions import db
from ..models import User

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/block/<int:user_id>', methods=['DELETE'])
def block_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get(user_id)
    if not user:
        abort(400)
    db.session.delete(user)
    db.session.commit()
    return '', 204
