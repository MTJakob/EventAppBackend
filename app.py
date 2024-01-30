from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from database import db
from resources.Event import blp as EventBlueprint
from resources.User import blp as UserBlueprint
from resources.EventParticipant import blp as EventParticipantBlueprint
from resources.Login import blp as LoginBlueprint
from resources.Register import blp as RegisterBlueprint
from resources.Search import blp as SearchBlueprint
import os


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Event Manager REST API"
    app.config["API_VERSION"] = "v1"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # disable for development purpose, should be switched on production env
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    db.init_app(app)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "test")
    # test on production is going to be str(secrets.SystemRandom().getrandbits(128))
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(EventBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(EventParticipantBlueprint)
    api.register_blueprint(LoginBlueprint)
    api.register_blueprint(RegisterBlueprint)
    api.register_blueprint(SearchBlueprint)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
