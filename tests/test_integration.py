"""Интеграционные тесты для API"""

import pytest
from app import create_app
from app.models import Todo


@pytest.fixture
def client():
    """Создаёт тестовый клиент Flask"""
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def cleanup():
    """Очищает данные после каждого теста"""
    yield
    Todo.clear_all()


class TestTodoAPI:
    """Тесты API задач"""

    def test_get_all_todos_empty(self, client):
        """Тест: получение пустого списка задач"""
        response = client.get('/api/todos')

        assert response.status_code == 200
        assert response.json == []

    def test_create_todo(self, client):
        """Тест: создание задачи"""
        response = client.post(
            '/api/todos',
            json={'title': 'Новая задача'}
        )

        assert response.status_code == 201
        assert response.json['title'] == 'Новая задача'
        assert response.json['completed'] == False

    def test_create_todo_without_title(self, client):
        """Тест: создание без заголовка (ошибка)"""
        response = client.post(
            '/api/todos',
            json={}
        )

        assert response.status_code == 400
        assert 'error' in response.json

    def test_get_todo_by_id(self, client):
        """Тест: получение задачи по ID"""
        # Сначала создаём
        client.post('/api/todos', json={'title': 'Задача'})

        # Получаем
        response = client.get('/api/todos/1')

        assert response.status_code == 200
        assert response.json['title'] == 'Задача'

    def test_get_todo_not_found(self, client):
        """Тест: задача не найдена"""
        response = client.get('/api/todos/999')

        assert response.status_code == 404

    def test_delete_todo(self, client):
        """Тест: удаление задачи"""
        # Создаём
        client.post('/api/todos', json={'title': 'Задача'})

        # Удаляем
        response = client.delete('/api/todos/1')

        assert response.status_code == 200

        # Проверяем, что удалена
        response = client.get('/api/todos/1')
        assert response.status_code == 404

    def test_complete_todo(self, client):
        """Тест: завершение задачи"""
        # Создаём
        client.post('/api/todos', json={'title': 'Задача'})

        # Завершаем
        response = client.put('/api/todos/1/complete')

        assert response.status_code == 200
        assert response.json['completed'] == True

    def test_get_all_todos_after_create(self, client):
        """Тест: получение всех задач после создания"""
        client.post('/api/todos', json={'title': 'Задача 1'})
        client.post('/api/todos', json={'title': 'Задача 2'})

        response = client.get('/api/todos')

        assert response.status_code == 200
        assert len(response.json) == 2