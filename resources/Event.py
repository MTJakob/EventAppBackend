from flask_restful import abort
from flask.views import MethodView
from database import db, User, Event as EventTable, Address, Category
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_smorest import Blueprint, abort
from schemas.PlainSchemas import EventSchema
from schemas.argumentSchemas import EventPostSchema, EventDeleteSchema, EventPutSchema
from schemas.responseSchemas import EventGetSchema
from datetime import datetime

blp = Blueprint("Event", __name__, description="Operations on events")


@blp.route('/event/<string:user_id>')
class Event(MethodView):

    @blp.arguments(EventPostSchema)
    def post(self, user_data, user_id):

        #category = Category.query.filter(Category.Name == user_data["eventCategory"]["Name"])
        address = Address \
        (
        Longitude=user_data["eventAddress"]["Longitude"],
        Latitude=user_data["eventAddress"]["Latitude"]
        )

        try:
            db.session.add(address)
            db.session.flush()
        except IntegrityError:
            abort(400, message="Submitted address cannot be added due to lack of data integrity")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the address.")

        event = EventTable \
        (Name=user_data["Name"],
         Price=user_data["Price"],
         StartDateTime=user_data["StartDateTime"],
         EndDateTime=user_data["EndDateTime"],
         Capacity=user_data["Capacity"],
         IDOrganiser=user_id,
         IDAddress=address.IDAddress#   ,
         #IDCategory=category.IDCategory
         )

        try:
            db.session.add(event)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Submitted event cannot be added due to lack of data integrity")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the event.")

        return {"message": "Event created successfully"}, 201

    @blp.arguments(EventPutSchema)
    def put(self, user_data, user_id):
        category = Category.query.filter(Category.Name == user_data["eventCategory"]["Name"])

        address = Address \
        (
        Name="proso je swinia", # do usuniecia!!!!
        Longitude=user_data["eventAddress"]["Longitude"],
        Latitude=user_data["eventAddress"]["Latitude"]
        )

        IDAddress = address.IDAddress,

        event = EventTable \
        (Name=user_data["Name"],
         Price=user_data["Price"],
         StartDateTime=user_data["StartDateTime"],
         EndDateTime=user_data["EndDateTime"],
         Capacity=user_data["Capacity"],
         IDOrganiser=user_id,
         IDCategory=category.IDCategory
         )
        try:
            db.session.add(event)
            db.session.flush()
            db.session.commit()
        except IntegrityError:
            abort(400, message="Submitted event cannot be updated due to lack of data integrity")
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the event.")

        return {"message": "Event updated successfully"}, 200

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
            abort(500, message="An error occurred while deleting the event.")
        return {"message": "Event deleted successfully"}, 202
