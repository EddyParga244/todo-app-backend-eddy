from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.todos_controller import add_todo, delete_todo, get_todo, reorder_todo, update_todo

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/api/todos', methods=["POST"])
@jwt_required()
def add_todo_route():
    return add_todo()

@todo_bp.route('/api/todos', methods=["GET"])
@jwt_required()
def get_todo_route():
    return get_todo()

@todo_bp.route('/api/todos/reorder', methods=["PUT"])
@jwt_required()
def reorder_todo_route():
    return reorder_todo()

@todo_bp.route('/api/todos/<string:todo_id>', methods=["DELETE"])
@jwt_required()
def delete_todo_route(todo_id):
    return delete_todo(todo_id)

@todo_bp.route('/api/todos/<string:todo_id>', methods=["PATCH"])
@jwt_required()
def update_todo_route(todo_id):
    return update_todo(todo_id)
