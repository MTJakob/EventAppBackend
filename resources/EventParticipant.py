from flask_restful import abort
from flask import request
from flask.views import MethodView
from database import db, User, EventParticipant as EventParticipantTable
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import and_
from flask_smorest import Blueprint, abort
from schemas.PlainSchemas import EventSchema
from schemas.argumentSchemas import EventParticipantDeleteSchema
from datetime import datetime

blp = Blueprint("EventParticipant", __name__, description="Operations on event participants")


@blp.route('/event participant/<string:user_id>')
class Event(MethodView):

    @blp.arguments()
    def post(self):
        return "EventParticipant has been successfully registered"

    #blp.arguments()
    def get(self):
        return "OK"

    @blp.arguments(EventParticipantDeleteSchema)
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
