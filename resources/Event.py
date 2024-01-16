from flask_restful import Api, Resource, abort, fields, marshal_with, reqparse
from flask import request
from database import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_smorest import Blueprint, abort

blp = Blueprint("Event", __name__, description="Operations on events")

#
# class Event(Resource):
#     def __init__(self):  # This method request pre-defined JSON file
#         parser = reqparse.RequestParser()
#         parser.add_argument("Name", type=str, help="User name", required=True)
#         parser.add_argument("Surname", type=str, help="User Surname", required=True)
#         parser.add_argument("Email", type=str, help="User Email", required=True)
#         parser.add_argument("DateOfBirth", type=str, help="User Surname", required=True)
#         parser.add_argument("Password", type=str, help="User Surname", required=True)
#         self.req_parser = parser


@blp.route('/event')
def post(self):
    request_data = request.getjson()
    name = self.req_parser.parse_args(strict=True).get("Name", None)
    surname = self.req_parser.parse_args(strict=True).get("Surname", None)
    email = self.req_parser.parse_args(strict=True).get("Email", None)
    date_of_birth = self.req_parser.parse_args(strict=True).get("DateOfBirth", None)
    password = self.req_parser.parse_args(strict=True).get("Password", None)

    #new_user = User(name, surname, email, date_of_birth, password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        abort(400, message="A store with that name already exists.",)
    except SQLAlchemyError:
        abort(500, message="An error occurred while inserting the item.")

    return "User is register successfully", 201


@blp.route("/event/put")
def put():
    return "OK", 201


@blp.route("/event/get")
def get():
    #data = Address.query.get_or_404(1)
    return data, 200
