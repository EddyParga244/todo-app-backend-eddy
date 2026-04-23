from logging.handlers import RotatingFileHandler
import os
import logging
from datetime import timedelta
import tempfile
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

from database.db import db
from database.extensions import bcrypt, jwt, limiter, scheduler
from helpers.cleanup import Cleanup
from models.user import User
from models.todo import Todo
from models.blacklist import Blacklist
from routes.auth_routes import auth_bp
from routes.todo_routes import todo_bp
from middleware.jwt_middleware import init_jwt_handlers

# Read .env variables
load_dotenv()
port = os.getenv("PORT")
secret_key = os.getenv("SECRET_KEY")
db_host= os.getenv("DB_HOST")
db_user= os.getenv("DB_USER")
db_password= os.getenv("DB_PASSWORD")
db_name= os.getenv("DB_NAME")
db_ssl_ca = os.getenv("DB_SSL_CA")
debug = os.getenv("DEBUG", "False") == "True"
origins = os.environ.get("CORS_ORIGINS", " https://todo-app-backend-eddy.onrender.com")

# SSL certificate
ssl_ca_file = None
if db_ssl_ca:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.crt', delete=False) as f:
        f.write(db_ssl_ca)
        ssl_ca_file = f.name

# Database URI
db_port = os.getenv("DB_PORT", "3306")
db_uri = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
if ssl_ca_file:
    db_uri += f'?ssl_ca={ssl_ca_file}'

# Start App
todoApp = Flask(__name__)

# Log configurations
todoApp.logger.setLevel(logging.ERROR)
handler = RotatingFileHandler("todo_app.log", maxBytes=5000000, backupCount=3)
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
todoApp.logger.addHandler(handler)

# CORS
CORS(todoApp, supports_credentials=True, origins=origins)

# App configurations
todoApp.config['SQLALCHEMY_DATABASE_URI'] = db_uri
todoApp.config['JWT_SECRET_KEY'] = secret_key
todoApp.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
todoApp.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
todoApp.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token'
todoApp.config['JWT_COOKIE_CSRF_PROTECT'] = False
todoApp.config['JWT_COOKIE_SAMESITE'] = "None"
todoApp.config['JWT_COOKIE_SECURE'] = True

# Initialize dependencies and db
db.init_app(todoApp)
bcrypt.init_app(todoApp)
jwt.init_app(todoApp)
limiter.init_app(todoApp)
scheduler.init_app(todoApp)
if not todoApp.config.get('TESTING'):
    scheduler.start()
scheduler.add_job(id='cleanup', func=Cleanup, trigger='interval', hours=24, args=[todoApp])
init_jwt_handlers(jwt)

# Create db tables
with todoApp.app_context():
    db.create_all()

# Register routes blueprints
todoApp.register_blueprint(auth_bp)
todoApp.register_blueprint(todo_bp)

# Global error handlers
@todoApp.errorhandler(500)
def internal_error(_error):
    return jsonify({"message": "Internal server error"}), 500

@todoApp.errorhandler(404)
def route_not_found(_error):
    return jsonify({"message": "Route not found"}), 404

# Run app
if __name__ == '__main__':
    todoApp.run(debug=debug, port=port)
