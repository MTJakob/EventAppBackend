from flask.views import MethodView
from database import Event as EventTable
from flask_smorest import Blueprint
from schemas.argumentSchemas import SearchPostSchema
from schemas.responseSchemas import EventGetSchema

blp = Blueprint("Search", __name__, description="Endpoint for searching the events")


@blp.route("/search")
class Search(MethodView):

    @blp.arguments(SearchPostSchema)
    @blp.response(200, EventGetSchema(many=True))
    def post(self, user_data):
        search_word = "%{}%".format(user_data["SearchWord"])
        events = EventTable.query.filter(EventTable.Name.like(search_word)).all()
        return events, 200
