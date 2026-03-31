from flask import Blueprint
from flask_jwt_extended import jwt_required
from database.extensions import limiter
from controllers.auth_controller import register, login, logout, refresh

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/register', methods=["POST"])
@limiter.limit("3/hour")
def register_route():
    return register()

@auth_bp.route('/api/auth/login', methods=["POST"])
@limiter.limit("5/minute")
def login_route():
    return login()

@auth_bp.route('/api/auth/logout', methods=["DELETE"])
@jwt_required()
def logout_route():
    return logout()

@auth_bp.route('/api/auth/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh_route():
    return refresh()
