from flask import jsonify

def init_jwt_handlers(jwt):
    @jwt.unauthorized_loader
    def unauthorized_callback(_error):
        return jsonify({"message": "Token missing"}), 401

    @jwt.invalid_token_loader
    def  invalid_callback(_error):
        return jsonify({"message": "Token is invalid"}), 400

    @jwt.expired_token_loader
    def expired_callback(_header, _data):
        return jsonify({"message": "Token is expired"}), 400
