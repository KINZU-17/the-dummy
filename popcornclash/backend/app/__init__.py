from flask import Flask
from flask_cors import CORS
from app.database.connection import init_db, seed_database


def create_app():
    app = Flask(__name__)
    CORS(app)

    init_db()
    seed_database()

    from app.routes.auth import auth_bp
    from app.routes.teams import teams_bp
    from app.routes.fixtures import fixtures_bp
    from app.routes.predictions import predictions_bp
    from app.routes.users import users_bp
    from app.routes.movies import movies_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(fixtures_bp)
    app.register_blueprint(predictions_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(movies_bp)

    return app
