from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.auth_controller import register, login, refresh

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/register', methods=["POST"])
def register_route():
    return register()

@auth_bp.route('/api/auth/login', methods=["POST"])
def login_route():
    return login()

@auth_bp.route('/api/auth/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh_route():
    return refresh()
