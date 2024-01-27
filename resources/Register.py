from flask_restful import abort
from flask.views import MethodView
from database import User as UserTable, db
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint
from passlib.context import CryptContext
from schemas.argumentSchemas import RegisterSchema
import os

blp = Blueprint("Register", __name__, description="Endpoint for register")

crypt_context = CryptContext(schemes=[os.getenv("CRYPT_CONTEXT")])


@blp.route("/register")
class Register(MethodView):

    @blp.arguments(RegisterSchema)
    def post(self, user_data):
        if UserTable.query.filter_by(Email=user_data["Email"]).first():
            abort(409, message="User with that email address already registered!")

        user = UserTable \
        (Email=user_data["Email"],
         Password=crypt_context.hash(user_data["Password"]),
         Name=user_data["Name"],
         Surname=user_data["Surname"],
         DateOfBirth=user_data["DateOfBirth"]
         )
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while registering the ussr.")
        return {"message": "User registered successfully"}, 201
