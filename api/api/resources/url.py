from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from api.api.schemas.user import URLShortenerSchema
from api.extensions import db


# TODO: add loggers


class URLShortenerResource(Resource):

    def post(self):
        schema = URLShortenerSchema()
        schema.validate(request.json)
        url = schema.load(request.json)

        db.session.add(url)
        db.session.commit()

        return {
            "msg": "URL for shortening has been created!",
            "url": schema.dump(url)
        }, 201
