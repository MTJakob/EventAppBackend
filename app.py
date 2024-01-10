from flask import Flask
from flask_restful import Api
import os
from database import db


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Event Manager REST API"
    app.config["API_VERSION"] = "v1"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    # disable for development purpose, should be switched on production env
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


@app.route('/')
def hello_world():  # put application's code here
    return 'API for Flutter Application!'


if __name__ == '__main__':
    app.run()
