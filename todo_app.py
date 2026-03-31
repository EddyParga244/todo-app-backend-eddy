import os
from datetime import timedelta
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

from database.db import db
from database.extensions import bcrypt, jwt, limiter
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

# Start App
todoApp = Flask(__name__)

# CORS
CORS(todoApp)

# App configurations
todoApp.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
todoApp.config['JWT_SECRET_KEY'] = secret_key
todoApp.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)

# Initialize dependencies and db
db.init_app(todoApp)
bcrypt.init_app(todoApp)
jwt.init_app(todoApp)
limiter.init_app(todoApp)
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
    todoApp.run(debug=True, port=port)
