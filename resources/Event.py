from flask_restful import abort
from flask.views import MethodView
from database import db, Event as EventTable, User, Address, Category as CategoryTable, \
    EventParticipant as EventParticipantTable
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_smorest import Blueprint, abort
from schemas.argumentSchemas import EventPostSchema, EventDeleteSchema, EventPutSchema, SearchPostSchema,\
    EventParticipantPostSchema, EventParticipantDeleteSchema
from schemas.responseSchemas import EventGetSchema
import json

blp = Blueprint("Event", __name__, description="Operations on events")


@blp.route('/event/<string:user_id>')
class Event(MethodView):

    @blp.arguments(EventPostSchema)
    def post(self, user_data, user_id):

        category = CategoryTable.query.filter_by(Name=user_data["eventCategory"]["Name"]).one_or_404()

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
         IDAddress=address.IDAddress,
         IDCategory=category.IDCategory
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

        event = EventTable.query.filter_by(IDEvent=user_data["IDEvent"]).one_or_404()

        if event.IDOrganiser != int(user_id):
            abort(403, message="Only organiser can alter the event")

        category = CategoryTable.query.filter_by(Name=user_data["eventCategory"]["Name"]).one_or_404()

        event.Name = user_data["Name"]
        event.Price = user_data["Price"]
        event.StartDateTime = user_data["StartDateTime"]
        event.EndDateTime = user_data["EndDateTime"]
        event.Capacity = user_data["Capacity"]
        event.IDCategory = category.IDCategory

        address = Address.query.filter(Address.IDAddress == event.IDAddress)

        address.Longitude = user_data["eventAddress"]["Longitude"]
        address.Latitude = user_data["eventAddress"]["Latitude"]

        try:
            db.session.commit()
        except IntegrityError:
            abort(400, message="Submitted event cannot be updated due to lack of data integrity")
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the event.")

        return {"message": "Event updated successfully"}, 200

    @blp.response(200, EventGetSchema(many=True))
    def get(self, user_id):
        events = EventTable.query.filter(EventTable.IDOrganiser == int(user_id))
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


@blp.route('/category')
class Category(MethodView):

    def post(self):

        f = open('categoryTree.json')

        categories = json.load(f)

        for i in categories:
            category = CategoryTable \
                (IDCategory=i["IDCategory"],
                 Name=i["Name"],
                 IDCategoryParent=i["IDCategoryParent"]
                 )

            try:
                db.session.add(category)
            except IntegrityError:
                abort(400, message="Submitted address cannot be added due to lack of data integrity")
            except SQLAlchemyError:
                abort(500, message="An error occurred while inserting the address.")

        try:
            db.session.commit()
        except IntegrityError:
            abort(400, message="Submitted address cannot be added due to lack of data integrity")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the address.")

        f.close()
        return "Categories are added to the database"


@blp.route("/search")
class Search(MethodView):

    @blp.arguments(SearchPostSchema)
    @blp.response(200, EventGetSchema(many=True))
    def post(self, user_data):
        search_word = "%{}%".format(user_data["SearchWord"])
        events = EventTable.query.filter(EventTable.Name.like(search_word)).all()
        return events, 200


@blp.route('/event participant/<string:user_id>')
class EventParticipant(MethodView):

    @blp.arguments(EventParticipantPostSchema)
    def post(self, user_data, user_id):
        Event.query.get_or_404(user_data["IDEvent"])
        User.query.get_or_404(user_id)

        event_participant = EventParticipantTable \
        (IDUser=user_id,
         IDEvent=user_data["IDEvent"]
         )
        try:
            db.session.add(event_participant)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Submitted address cannot be added due to lack of data integrity")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the address.")
        return "EventParticipant has been successfully registered"

    @blp.response(200, EventGetSchema(many=True))
    def get(self, user_id):
        events = Event.query.filter(EventParticipantTable.IDUser == int(user_id), Event.IDEvent == EventParticipantTable.IDEvent)
        return events, 200

    @blp.arguments(EventParticipantDeleteSchema)
    def delete(self, user_data, user_id):
        event_participant = EventParticipantTable.query.filter_by(IDEvent=user_data["IDEvent"],
                 IDUser=int(user_id)).one_or_404()
        try:
            db.session.delete(event_participant)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while unsubscribing form the event.")
        return {"message": "Participant successfully unsubscribed from the event."}, 202

