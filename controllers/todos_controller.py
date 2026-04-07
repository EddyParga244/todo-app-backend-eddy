import uuid
from flask import jsonify, request, current_app
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from models.todo import Todo
from models.user import User
from schemas.todo_schema import TodoSchema

def add_todo():
    # Get data from frontend
    data = request.get_json()
    text = data.get("text")
    completed = data.get("completed")

    # Get email from token
    user_id = get_jwt_identity()

    # Verify if user already exists in database (by token)
    existing_user = User.query.filter_by(email=user_id).first()

    # if it doesn't exist return error message
    if not existing_user:
        return jsonify({"message": "User not found"}), 404

    # Count todo position
    position = db.session.query(func.count(Todo.id)).filter_by(user_id=existing_user.id).scalar()

    # Validate todo schema and handle errors
    schema = TodoSchema()

    try:
        schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Add todo in database
    new_todo = Todo(id=str(uuid.uuid4()), user_id=existing_user.id, text=text, completed=completed, position=position)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"message": "New todo added successfully"}), 201

def get_todo():
    # Get email from token
    user_id = get_jwt_identity()

    # Verify if user already exists in database (by token)
    existing_user = User.query.filter_by(email=user_id).first()

     # if it doesn't exist return error message
    if not existing_user:
        return jsonify({"message": "User not found"}), 404

    # Get todos from database and order by position
    get_todos = db.select(Todo).filter_by(user_id=existing_user.id).order_by(Todo.position)
    stored_todos = db.session.execute(get_todos).scalars().all()

    # Serialize todos to JSON
    schema = TodoSchema(many=True)
    return jsonify(schema.dump(stored_todos)), 200

def delete_todo(todo_id):

    # Verify if todo id already exists in database
    existing_todo = Todo.query.filter_by(id=todo_id).first()

    # if it doesn't exist return error message
    if not existing_todo:
        return jsonify({"message": "Todo not found"}), 404

    # Get email from token
    user_id = get_jwt_identity()

    # Verify if user already exists in database (by token)
    existing_user = User.query.filter_by(email=user_id).first()

    # Verify todo belong to user
    if existing_todo.user_id == existing_user.id:
        try:
            db.session.delete(existing_todo)

            # Reorder todo's position
            todos_to_update = Todo.query.filter(Todo.user_id == existing_user.id, Todo.position > existing_todo.position).all()
            for todo in todos_to_update:
                todo.position -= 1

            db.session.commit()
            return jsonify({"message": "Todo deleted successfully"}), 200
        except SQLAlchemyError as err:
            db.session.rollback()
            current_app.logger.error("Error in %s %s: %s", request.method, request.url, err)
            return jsonify({"Error": f"{err}"}), 500

    return  jsonify({"message": "Todo doesn't belong to user"}), 400

def update_todo(todo_id):
    # Get data from frontend
    data = request.get_json()
    text = data.get("text")
    completed = data.get("completed")

    # Verify if todo id already exists in database
    existing_todo = Todo.query.filter_by(id=todo_id).first()

    # if it doesn't exist return error message
    if not existing_todo:
        return jsonify({"message": "Todo not found"}), 404

    # Get email from token
    user_id = get_jwt_identity()

    # Verify if user already exists in database (by token)
    existing_user = User.query.filter_by(email=user_id).first()

    # Verify todo belong to user
    if existing_todo.user_id == existing_user.id:
        try:
            if text is not None:
                existing_todo.text = text

            if completed is not None:
                existing_todo.completed = completed

            db.session.commit()
            return jsonify({"message": "Todo updated successfully"}), 200

        except SQLAlchemyError as err:
            db.session.rollback()
            current_app.logger.error("Error in %s %s: %s", request.method, request.url, err)
            return jsonify({"Error": f"{err}"}), 500

    return  jsonify({"message": "Todo doesn't belong to user"}), 400

def reorder_todo():
    # Get data from frontend
    data = request.get_json().get("data")

    # Verify data from frontend
    if not data:
        return jsonify({"message": "Todo required"}), 400

    # Get email from token
    user_id = get_jwt_identity()

    # Verify if user already exists in database (by token)
    existing_user = User.query.filter_by(email=user_id).first()

    # Reorder todo's position
    for index, todo_id in enumerate(data):
        todo = Todo.query.filter_by(id=todo_id, user_id=existing_user.id).first()
        if todo:
            todo.position = index

    db.session.commit()
    return jsonify({"message": "Todo reordered successfully"}), 200
