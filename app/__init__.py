from flask import Flask


def create_app():
    """Создаёт и настраивает Flask приложение"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key'

    # Регистрируем маршруты
    from app.routes import todo_bp
    app.register_blueprint(todo_bp)

    return app