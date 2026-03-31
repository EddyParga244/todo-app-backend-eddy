import os
from datetime import timedelta
from flask import Flask
from dotenv import load_dotenv

from database.db import db
from database.extensions import bcrypt, jwt
from models.user import User
from models.todo import Todo
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

# App configurations
todoApp.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
todoApp.config['JWT_SECRET_KEY'] = secret_key
todoApp.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)

# Initialize dependencies and db
db.init_app(todoApp)
bcrypt.init_app(todoApp)
jwt.init_app(todoApp)
init_jwt_handlers(jwt)

# Endpoints
# @todoApp.route('/')

# Create db tables
with todoApp.app_context():
    db.create_all()

# Register routes blueprints
todoApp.register_blueprint(auth_bp)
todoApp.register_blueprint(todo_bp)

# Run app
if __name__ == '__main__':
    todoApp.run(debug=True, port=port)
