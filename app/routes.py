"""Маршруты API"""

from flask import Blueprint, jsonify, request
from app.models import Todo

todo_bp = Blueprint('todo', __name__, url_prefix='/api/todos')


@todo_bp.route('', methods=['GET'])
def get_all_todos():
    """Получить все задачи"""
    todos = Todo.get_all()
    return jsonify([todo.to_dict() for todo in todos]), 200


@todo_bp.route('', methods=['POST'])
def create_todo():
    """Создать новую задачу"""
    data = request.get_json()

    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400

    todo = Todo.create(data['title'])
    return jsonify(todo.to_dict()), 201


@todo_bp.route('/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Получить задачу по ID"""
    todo = Todo.get_by_id(todo_id)

    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    return jsonify(todo.to_dict()), 200


@todo_bp.route('/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Удалить задачу"""
    if Todo.delete(todo_id):
        return jsonify({'message': 'Todo deleted'}), 200

    return jsonify({'error': 'Todo not found'}), 404


@todo_bp.route('/<int:todo_id>/complete', methods=['PUT'])
def complete_todo(todo_id):
    """Отметить задачу как выполненную"""
    todo = Todo.get_by_id(todo_id)

    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    todo.completed = True
    return jsonify(todo.to_dict()), 200