from flask_restful import abort
from flask.views import MethodView
from database import User as UserTable
from flask_smorest import Blueprint
from passlib.context import CryptContext
from schemas.argumentSchemas import LoginSchema
from flask_jwt_extended import create_access_token
import os

blp = Blueprint("Login", __name__, description="Endpoint on login")

crypt_context = CryptContext(schemes=[os.getenv("CRYPT_CONTEXT")])


@blp.route("/login")
class User(MethodView):

    @blp.arguments(LoginSchema)
    def post(self, user_data):
        user = UserTable.query.filter_by(Email=user_data["Email"]).one_or_404()
        if crypt_context.verify(user_data["Password"], user.Password):
            access_token = create_access_token(identity=user.IDUser)
            return {"access_token": access_token}, 200
        abort(401, message="Invalid email or password.")
