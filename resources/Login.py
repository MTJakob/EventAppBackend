from flask_restful import abort
from flask.views import MethodView
from database import db, User as UserTable
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint
from passlib.context import CryptContext
from schemas.argumentSchemas import LoginSchema, ChangePasswordSchema
from flask_jwt_extended import create_access_token
import os

blp = Blueprint("Login", __name__, description="Endpoint for login")

crypt_context = CryptContext(schemes=[os.getenv("CRYPT_CONTEXT")])


@blp.route("/login")
class User(MethodView):

    @blp.arguments(LoginSchema)
    def post(self, user_data):
        user = UserTable.query.filter_by(Email=user_data["Email"]).one_or_404()
        if crypt_context.verify(user_data["Password"], user.Password):
            access_token = create_access_token(identity=user.IDUser)
            return {"message": "User logged in successfully",
                    "user_id": user.IDUser,
                    "access_token": access_token}, 200
        abort(401, message="Invalid email or password.")

    @blp.arguments(ChangePasswordSchema)
    def put(self, user_data):
        user = UserTable.query.filter_by(IDUser=user_data["IDUser"]).one_or_404()
        if crypt_context.verify(user_data["OldPassword"], user.Password):
            user.Password = crypt_context.hash(user_data["NewPassword"])
        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while changing the password.")
        abort(401, message="Invalid old password.")
