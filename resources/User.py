from flask_restful import abort
from flask import request
from flask.views import MethodView
from database import db, User, Event as EventTable
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_smorest import Blueprint, abort
from schemas.PlainSchemas import EventSchema, PlainUserSchema
from schemas.argumentSchemas import EventGetSchema
from passlib.context import CryptContext
from datetime import datetime
import os

blp = Blueprint("User", __name__, description="Operations on users")

crypt_context = CryptContext(schemes=[os.getenv("CRYPT_CONTEXT")])
@blp.route('/user') #/<string:name>
class Event(MethodView):

    #@blp.arguments(201, PlainUserSchema(many=True))
    def post(self):

        return "User has been successfully registered"

    #@blp.arguments()
    def put(self):
        #crypt_context.default_scheme()
        p = User(Email='dupadusdepa@dupa.com',
                    Password=crypt_context.hash("password"),
                    Name="Oleczek",
                    Surname='Znazwizkiem',
                 DateOfBirth=datetime(2002, 10, 5))
        #p = Category(Name="Sporty i Rekreacje")
        #try:
        db.session.add(p)
        db.session.commit()
        # except SQLAlchemyError:
        #     abort(500, message="An error occurred while inserting the item.")
        return "User data changed successfully"

    @blp.response(200, PlainUserSchema(many=True))
    def get(self):
        data = User.query.all()
        return data
