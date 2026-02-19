"""Модель данных для задач"""

# Хранилище задач (в памяти, для простоты)
todos = {}
next_id = 1


class Todo:
    """Класс задачи"""

    def __init__(self, title, completed=False):
        global next_id
        self.id = next_id
        self.title = title
        self.completed = completed
        next_id += 1

    def to_dict(self):
        """Преобразует задачу в словарь"""
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed
        }

    @classmethod
    def create(cls, title):
        """Создаёт новую задачу"""
        todo = cls(title)
        todos[todo.id] = todo
        return todo

    @classmethod
    def get_all(cls):
        """Возвращает все задачи"""
        return list(todos.values())

    @classmethod
    def get_by_id(cls, todo_id):
        """Возвращает задачу по ID"""
        return todos.get(todo_id)

    @classmethod
    def delete(cls, todo_id):
        """Удаляет задачу"""
        if todo_id in todos:
            del todos[todo_id]
            return True
        return False

    @classmethod
    def clear_all(cls):
        """Очищает все задачи (для тестов)"""
        global todos, next_id
        todos = {}
        next_id = 1