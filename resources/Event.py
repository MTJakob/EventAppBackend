from flask_restful import abort
from flask.views import MethodView
from database import db, User, Event as EventTable
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_smorest import Blueprint, abort
from schemas.PlainSchemas import EventSchema
from schemas.argumentSchemas import EventPostSchema, EventDeleteSchema
from schemas.argumentSchemas import EventGetSchema
from datetime import datetime

blp = Blueprint("Event", __name__, description="Operations on events")


@blp.route('/event/<string:user_id>')
class Event(MethodView):

    @blp.arguments(EventPostSchema)
    def post(self, user_data, user_id):
        event = EventTable \
        (Name=user_data["Name"],
         Price=user_data["Price"],
         StartDateTime=user_data["StartDateTime"],
         EndDateTime=user_data["EndDateTime"],
         Capacity=user_data["Capacity"],
         IDOrganiser=user_id
         )
        try:
            db.session.add(event)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Submitted event cannot be added due to lack of data integrity")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the event.")
        return {"message": "Event created successfully"}, 201

    #@blp.response(200, AddressSchema(many=True))
    def put(self):
        p = EventTable(Name='TestEventIDCategory0', Capacity=60,
                       StartDateTime=datetime.now(),
                       EndDateTime=datetime.now(),
                       Price=40.0, IDCategory=0)
        #p = Category(Name="Sporty i Rekreacje")
        try:
            db.session.add(p)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        return "OK", 201

    @blp.response(200, EventSchema(many=True))
    def get(self, user_id):
        data = EventTable.query.all()  # .filter(EventParticipant.IDUser == user_id)
        return data, 200

    @blp.arguments(EventDeleteSchema)
    def delete(self):

        return "OK"
