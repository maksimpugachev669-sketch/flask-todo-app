"""Системные тесты (полные сценарии использования)"""

import pytest
from app import create_app
from app.models import Todo


@pytest.fixture
def app():
    """Создаёт приложение для тестов"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Создаёт тестовый клиент"""
    return app.test_client()


@pytest.fixture(autouse=True)
def cleanup():
    """Очищает данные после каждого теста"""
    yield
    Todo.clear_all()


class TestSystemScenarios:
    """Системные тесты - полные сценарии"""

    def test_full_todo_workflow(self, client):
        """
        Сценарий: Полный цикл работы с задачей

        1. Создаём задачу
        2. Получаем список задач
        3. Получаем задачу по ID
        4. Отмечаем как выполненную
        5. Удаляем задачу
        6. Проверяем, что удалена
        """
        # 1. Создаём
        create_response = client.post(
            '/api/todos',
            json={'title': 'Системный тест'}
        )
        assert create_response.status_code == 201
        todo_id = create_response.json['id']

        # 2. Получаем список
        list_response = client.get('/api/todos')
        assert list_response.status_code == 200
        assert len(list_response.json) == 1

        # 3. Получаем по ID
        get_response = client.get(f'/api/todos/{todo_id}')
        assert get_response.status_code == 200
        assert get_response.json['title'] == 'Системный тест'

        # 4. Завершаем
        complete_response = client.put(f'/api/todos/{todo_id}/complete')
        assert complete_response.status_code == 200
        assert complete_response.json['completed'] == True

        # 5. Удаляем
        delete_response = client.delete(f'/api/todos/{todo_id}')
        assert delete_response.status_code == 200

        # 6. Проверяем удаление
        check_response = client.get(f'/api/todos/{todo_id}')
        assert check_response.status_code == 404

    def test_multiple_todos_workflow(self, client):
        """
        Сценарий: Работа с несколькими задачами

        1. Создаём 3 задачи
        2. Проверяем количество
        3. Завершаем 2 задачи
        4. Удаляем 1 задачу
        5. Проверяем итоговое состояние
        """
        # 1. Создаём 3 задачи
        for i in range(3):
            client.post('/api/todos', json={'title': f'Задача {i + 1}'})

        # 2. Проверяем количество
        response = client.get('/api/todos')
        assert len(response.json) == 3

        # 3. Завершаем 2 задачи
        client.put('/api/todos/1/complete')
        client.put('/api/todos/2/complete')

        # 4. Удаляем 1 задачу
        client.delete('/api/todos/3')

        # 5. Проверяем итог
        response = client.get('/api/todos')
        assert len(response.json) == 2

        # Проверяем, что оставшиеся задачи имеют правильные данные
        todos = response.json
        completed_count = sum(1 for t in todos if t['completed'])
        assert completed_count == 2

    def test_error_handling_workflow(self, client):
        """
        Сценарий: Обработка ошибок

        1. Пытаемся получить несуществующую задачу
        2. Пытаемся создать задачу без заголовка
        3. Пытаемся удалить несуществующую задачу
        4. Пытаемся завершить несуществующую задачу
        """
        # 1. Получение несуществующей
        response = client.get('/api/todos/999')
        assert response.status_code == 404

        # 2. Создание без заголовка
        response = client.post('/api/todos', json={})
        assert response.status_code == 400

        # 3. Удаление несуществующей
        response = client.delete('/api/todos/999')
        assert response.status_code == 404

        # 4. Завершение несуществующей
        response = client.put('/api/todos/999/complete')
        assert response.status_code == 404