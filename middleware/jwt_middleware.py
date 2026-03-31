from flask import jsonify

from database.db import db
from models.blacklist import Blacklist

def init_jwt_handlers(jwt):
    @jwt.unauthorized_loader
    def unauthorized_callback(_error):
        return jsonify({"message": "Token missing"}), 401

    @jwt.invalid_token_loader
    def invalid_callback(_error):
        return jsonify({"message": "Token is invalid"}), 400

    @jwt.expired_token_loader
    def expired_callback(_header, _data):
        return jsonify({"message": "Token is expired"}), 400

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(Blacklist.jti).filter_by(jti=jti).scalar()

        return token is not None

    @jwt.revoked_token_loader
    def revoked_callback(_header, _data):
        return jsonify({"message": "Token has been revoked"}), 401
    