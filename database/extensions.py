from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

jwt = JWTManager()
bcrypt = Bcrypt()
marshmallow = Marshmallow()
