from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from api.api.resources import URLShortenerResource

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


# api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
# api.add_resource(UserList, "/users", endpoint="users")
api.add_resource(URLShortenerResource, "/url", "/url/<short_url_id>", endpoint="url")


@blueprint.before_app_request
def register_views():
    # apispec.components.schema("UserSchema", schema=UserSchema)
    # apispec.path(view=UserResource, app=current_app)
    # apispec.path(view=UserList, app=current_app)
    pass


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
