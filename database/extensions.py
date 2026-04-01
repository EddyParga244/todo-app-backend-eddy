from flask_apscheduler import APScheduler
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow

jwt = JWTManager()
bcrypt = Bcrypt()
marshmallow = Marshmallow()
limiter = Limiter(get_remote_address)
scheduler = APScheduler()
