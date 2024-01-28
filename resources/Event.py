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

    @blp.response(200, EventSchema)
    def put(self):

        return "OK", 201

    @blp.response(200, EventGetSchema(many=True))
    def get(self, user_id):
        events = EventTable.query.all()  # .filter(EventParticipant.IDUser == user_id)
        return events, 200

    @blp.arguments(EventDeleteSchema)
    @blp.alt_response(404, description="Event with that ID not found")
    def delete(self, user_data, user_id):
        event = EventTable.query.get_or_404(user_data["IDEvent"])
        if event.IDOrganiser != int(user_id):
            abort(403, message="Only organiser can delete the event")
        try:
            db.session.delete(event)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        return {"message": "Event deleted successfully"}, 202
