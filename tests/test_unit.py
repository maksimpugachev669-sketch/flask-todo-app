"""Модульные тесты для модели Todo"""

import pytest
from app.models import Todo


class TestTodoModel:
    """Тесты модели Todo"""

    def setup_method(self):
        """Очищает данные перед каждым тестом"""
        Todo.clear_all()

    def test_create_todo(self):
        """Тест: создание задачи"""
        todo = Todo.create("Купить молоко")

        assert todo.id == 1
        assert todo.title == "Купить молоко"
        assert todo.completed == False

    def test_todo_to_dict(self):
        """Тест: преобразование в словарь"""
        todo = Todo.create("Задача")
        data = todo.to_dict()

        assert data['id'] == 1
        assert data['title'] == "Задача"
        assert data['completed'] == False

    def test_get_all_todos(self):
        """Тест: получение всех задач"""
        Todo.create("Задача 1")
        Todo.create("Задача 2")

        todos = Todo.get_all()

        assert len(todos) == 2

    def test_get_by_id(self):
        """Тест: получение задачи по ID"""
        todo = Todo.create("Задача")
        found = Todo.get_by_id(1)

        assert found == todo
        assert found.title == "Задача"

    def test_get_by_id_not_found(self):
        """Тест: задача не найдена"""
        found = Todo.get_by_id(999)

        assert found is None

    def test_delete_todo(self):
        """Тест: удаление задачи"""
        Todo.create("Задача")

        result = Todo.delete(1)

        assert result == True
        assert Todo.get_by_id(1) is None

    def test_delete_not_found(self):
        """Тест: удаление несуществующей задачи"""
        result = Todo.delete(999)

        assert result == False

    def test_complete_todo(self):
        """Тест: завершение задачи"""
        todo = Todo.create("Задача")
        todo.completed = True

        assert todo.completed == True