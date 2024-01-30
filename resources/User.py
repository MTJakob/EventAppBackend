from flask_restful import abort
from flask.views import MethodView
from database import db, User as UserTable
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort
from schemas.PlainSchemas import PlainUserSchema


blp = Blueprint("User", __name__, description="Operations on users")


@blp.route('/user/<string:user_id>')
class User(MethodView):

    @blp.arguments(PlainUserSchema)
    def put(self, user_data, user_id):
        user_to_modify = UserTable.query.filter_by(IDUser=user_id).one_or_404()
        user_to_modify.Name = user_data["Name"]
        user_to_modify.Surname = user_data["Surname"]
        user_to_modify.Email = user_data["Email"]
        user_to_modify.DateOfBirth = user_data["DateOfBirth"]
        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating user data.")
        return {"message": "User data updated successfully"}, 200

    @blp.response(200, PlainUserSchema)
    def get(self, user_id):
        data = UserTable.query.get_or_404(user_id)
        return data
