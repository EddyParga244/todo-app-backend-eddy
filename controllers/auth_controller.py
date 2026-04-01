import uuid
from flask import make_response, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from marshmallow import ValidationError
from database.db import db
from database.extensions import bcrypt
from helpers.blacklist_tokens import blacklist_tokens
from models.user import User
from schemas.auth_schema import ChangePasswordSchema, DeleteUserSchema, UserSchema

def register():
    # Get data from frontend
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Validate user schema and handle errors
    schema = UserSchema()

    try:
        schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    #Encrypt password
    hashed_password = bcrypt.generate_password_hash(password)

    # Verify if user already exists in database
    existing_user = User.query.filter_by(email=email).first()

    # if it exists return error message, else register user in database
    if existing_user:
        return jsonify({"message": "User already registered with this email"}), 409

    new_user = User(id=str(uuid.uuid4()),email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Register successful"}), 201

def login():
    # Get data from frontend
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Validate user schema and handle errors
    schema = UserSchema()

    try:
        schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Verify user from database
    user_db = User.query.filter_by(email=email).first()

    if not user_db:
        return jsonify({"message": "Invalid credentials"}), 404

    # Get hashed password from database
    hashed_password_db = user_db.password

    # Compare hashed password with frontend password
    checked_password = bcrypt.check_password_hash(hashed_password_db, password)

    # Generate access token and Authorize Login
    if checked_password:
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        response = make_response(jsonify(access_token=access_token, refresh_token=refresh_token, message="Login successful"), 200)
        response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='Strict')
        return response

    return  jsonify({"message": "Invalid credentials"}), 404

def logout():
    # Blacklist access and refresh tokens
    blacklist_tokens()
    return jsonify({"message": "Logout successful"}), 200

def change_password():
    # Get data from frontend
    data = request.get_json()
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    # Get email from token
    user_id = get_jwt_identity()

    # Verify if user already exists in database (by token)
    user_db = User.query.filter_by(email=user_id).first()

    if not user_db:
        return jsonify({"message": "Invalid credentials"}), 404

    # Validate user schema and handle errors
    schema = ChangePasswordSchema()

    try:
        schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Compare stored database password with frontend current password
    if current_password and user_db.password:
        checked_password = bcrypt.check_password_hash(user_db.password, current_password)
        if not checked_password:
            return jsonify({"message": "Invalid credentials"}), 401
        
        # Hash new password and update it to database
        hashed_new_password = bcrypt.generate_password_hash(new_password)
        user_db.password = hashed_new_password
        db.session.commit()
    return jsonify({"message": "Password updated successfully"}), 200

def refresh():
    # Generate acess token using refresh token
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

def delete_account():
    # Get data from frontend
    data = request.get_json()
    password = data.get("password")

    # Get user from token
    user_id = get_jwt_identity()

    # Verify user from database
    user_db = User.query.filter_by(email=user_id).first()
    if not user_db:
        return jsonify({"message": "Invalid credentials"}), 401
    
    # Verify password hash from database
    checked_password = bcrypt.check_password_hash(user_db.password, password)
    if not checked_password:
        return jsonify({"message": "Invalid credentials"}), 401

    # Validate user schema and handle errors
    schema = DeleteUserSchema()

    try:
        schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Delete user and blacklist tokens
    blacklist_tokens()
    db.session.delete(user_db)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
    