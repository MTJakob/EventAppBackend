from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from database import db
from resources.Event import blp as EventBlueprint
from resources.User import blp as UserBlueprint
from resources.EventParticipant import blp as EventParticipantBlueprint
from resources.Login import blp as LoginBlueprint
from resources.Register import blp as RegisterBlueprint
from blocklist import BLOCKLIST
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

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST  # jti JWT ID

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"message": "The token has been revoked."}
            ), 401
        )

    @jwt.expired_token_loader()
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"message": "The token has expired."}
            ), 401
        )

    @jwt.invalid_token_loader()
    def expired_token_callback(error):
        return (
            jsonify(
                {"message": "Verification of the token failed."}
            ), 401
        )

    @jwt.unauthorized_loader()
    def missing_token_callback(error):
        return (
            jsonify(
                {"message": "No token is supplied with the request."}
            ), 401
        )

    @jwt.needs_fresh_token_loader()
    def needs_fresh_token_callback(error):
        return (
            jsonify(
                {"message": "Token is not fresh, for ths endpoint you have to supply fresh token."}
            ), 401
        )

    with app.app_context():
        db.create_all()

    api.register_blueprint(EventBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(EventParticipantBlueprint)
    api.register_blueprint(LoginBlueprint)
    api.register_blueprint(RegisterBlueprint)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
