from flask_restful import abort
from flask import request
from flask.views import MethodView
from database import db, User, EventParticipant as EventParticipantTable, Event
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import and_
from flask_smorest import Blueprint, abort
from schemas.argumentSchemas import EventParticipantDeletePostSchema
from datetime import datetime

blp = Blueprint("EventParticipant", __name__, description="Operations on event participants")


@blp.route('/event participant/<string:user_id>')
class EventParticipant(MethodView):

    @blp.arguments(EventParticipantDeletePostSchema)
    def post(self, user_data, user_id):
        Event.query.get_or_404(user_data["IDEvent"])
        User.query.get_or_404(int(user_id))

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

    @blp.response(200)
    def get(self):
        return "OK"

    @blp.arguments(EventParticipantDeletePostSchema)
    def delete(self, user_data, user_id):
        event_participant = EventParticipantTable.query.one_or_404(
            and_(EventParticipantTable.IDEvent == user_data["IDEvent"],
                 EventParticipantTable.IDUser == user_id))
        try:
            db.session.delete(event_participant)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while unsubscribing form the event.")
        return {"message": "Participant successfully unsubscribed from the event."}, 202
