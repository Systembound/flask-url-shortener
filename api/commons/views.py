from flask import redirect, Blueprint
from flask.views import MethodView

from api import extensions

blueprint = Blueprint("shortcuts", __name__, url_prefix="/")


# create view for redirecting and hitting increase visits
class ShortUrlVisits(MethodView):

    def __init__(self, model=None):
        if model is None:
            from api.models import api as api_models
            self.model = api_models.Url
        else:
            self.model = model

    def get_an_item(self, short_url_id):
        return self.model.query.filter_by(
            new=short_url_id
        ).first_or_404()

    def get(self, short_url_id):
        # fetch its object from model and return 404 if not found else
        #  increase its visits and redirect to its url
        obj = self.get_an_item(short_url_id)
        # increase its visits
        obj.hits += 1
        # commit changes
        extensions.db.session.commit()

        # redirect to its url
        return redirect(obj.url)


def register_views():
    short_url_visits = ShortUrlVisits.as_view("short_url_visits")
    blueprint.add_url_rule(
        "/<short_url_id>",
        view_func=short_url_visits,
    )


register_views()
